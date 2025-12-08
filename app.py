from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import json

# Configurar FFmpeg antes de importar transcriber
import imageio_ffmpeg
os.environ['PATH'] = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe()) + os.pathsep + os.environ['PATH']

from transcriber import process_video
from humanizer import humanize_text, improve_readability
from summarizer import summarize_text, extract_keywords
from media_compressor import compress_image, convert_image_format, compress_video, convert_video_format, get_media_info

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'message': 'Archivo subido exitosamente'
        })
    
    return jsonify({'error': 'Formato de archivo no permitido'}), 400

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    filename = data.get('filename')
    generate_summary = data.get('generate_summary', True)
    
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        result = process_video(filepath, generate_summary)
        return jsonify({
            'success': True,
            'transcription': result['transcription'],
            'summary': result.get('summary', ''),
            'output_file': result['output_file']
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@app.route('/list-outputs')
def list_outputs():
    files = []
    if os.path.exists(app.config['OUTPUT_FOLDER']):
        for f in os.listdir(app.config['OUTPUT_FOLDER']):
            if f.endswith('.txt'):
                files.append(f)
    return jsonify({'files': files})

@app.route('/humanize', methods=['POST'])
def humanize():
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        humanized = humanize_text(text)
        improved = improve_readability(humanized)
        
        return jsonify({
            'success': True,
            'humanized_text': improved
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    text = data.get('text', '')
    percentage = data.get('percentage', 30)
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        summary = summarize_text(text, percentage=percentage)
        keywords = extract_keywords(text, num_keywords=10)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'keywords': keywords,
            'original_length': len(text),
            'summary_length': len(summary)
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/compress-image', methods=['POST'])
def compress_image_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    quality = request.form.get('quality', 75, type=int)
    max_width = request.form.get('max_width', 1920, type=int)
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_filename = f"compressed_{os.path.splitext(filename)[0]}.jpg"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        file.save(input_path)
        result = compress_image(input_path, output_path, quality=quality, max_width=max_width)
        
        if result['success']:
            result['download_file'] = output_filename
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/convert-image', methods=['POST'])
def convert_image_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    target_format = request.form.get('format', 'webp')
    quality = request.form.get('quality', 80, type=int)
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_filename = f"converted_{os.path.splitext(filename)[0]}.{target_format}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        file.save(input_path)
        result = convert_image_format(input_path, output_path, target_format=target_format, quality=quality)
        
        if result['success']:
            result['download_file'] = output_filename
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/compress-video', methods=['POST'])
def compress_video_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    quality = request.form.get('quality', 'medium')

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_filename = f"compressed_{os.path.splitext(filename)[0]}.mp4"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        print(f"Guardando archivo: {input_path}")
        file.save(input_path)

        print(f"Comprimiendo video: {filename}")
        result = compress_video(input_path, output_path, quality=quality)

        if result['success']:
            result['download_file'] = output_filename
            print(f"Video comprimido exitosamente")
        else:
            print(f"Error al comprimir: {result.get('error')}")

        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/convert-video', methods=['POST'])
def convert_video_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    target_format = request.form.get('format', 'mp4')

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_filename = f"converted_{os.path.splitext(filename)[0]}.{target_format}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        print(f"Guardando archivo: {input_path}")
        file.save(input_path)

        print(f"Convirtiendo video: {filename} a {target_format}")
        result = convert_video_format(input_path, output_path, target_format=target_format)

        if result['success']:
            result['download_file'] = output_filename
            print(f"Video convertido exitosamente")
        else:
            print(f"Error al convertir: {result.get('error')}")

        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
