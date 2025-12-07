import os
import whisper
from moviepy import VideoFileClip
from datetime import datetime
import torch
import imageio_ffmpeg

# Configurar la ruta de FFmpeg
os.environ['PATH'] = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe()) + os.pathsep + os.environ['PATH']

def extract_audio(video_path, audio_output_path):
    """
    Extrae el audio de un archivo de video MP4
    """
    print(f"Extrayendo audio de {video_path}...")
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_output_path, codec='libmp3lame')
    video.close()
    print(f"Audio extraído exitosamente a {audio_output_path}")
    return audio_output_path

def transcribe_audio(audio_path, model_size='base'):
    """
    Transcribe el audio usando Whisper de OpenAI
    model_size: 'tiny', 'base', 'small', 'medium', 'large'
    """
    print(f"Cargando modelo Whisper ({model_size})...")
    
    # Detectar si hay GPU disponible
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Usando dispositivo: {device}")
    
    model = whisper.load_model(model_size, device=device)
    
    print(f"Transcribiendo audio...")
    # Usar fp16=False para evitar problemas en CPU
    result = model.transcribe(audio_path, language='es', verbose=True, fp16=False)
    
    transcription = result['text']
    print(f"Transcripción completada. Total de caracteres: {len(transcription)}")
    
    return transcription

def generate_summary(text, max_sentences=10):
    """
    Genera un resumen del texto transcrito
    Nota: Esta es una versión simple. Para mejores resultados, considera usar
    modelos de lenguaje como GPT o BERT para resumir.
    """
    sentences = text.split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Toma las primeras frases como resumen simple
    # En producción, usarías un modelo de IA para resumir
    summary_sentences = sentences[:max_sentences]
    summary = '. '.join(summary_sentences) + '.'
    
    return summary

def save_to_file(content, output_path):
    """
    Guarda el contenido en un archivo de texto
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Contenido guardado en {output_path}")

def process_video(video_path, generate_summary_flag=True, model_size='base'):
    """
    Procesa un video completo: extrae audio, transcribe y genera resumen
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = os.path.splitext(os.path.basename(video_path))[0]
    
    # Rutas de salida
    audio_path = f"outputs/{base_filename}_{timestamp}_audio.mp3"
    output_text_file = f"outputs/{base_filename}_{timestamp}_transcription.txt"
    
    # Paso 1: Extraer audio
    extract_audio(video_path, audio_path)
    
    # Paso 2: Transcribir audio
    transcription = transcribe_audio(audio_path, model_size)
    
    # Paso 3: Generar resumen (opcional)
    summary = ""
    if generate_summary_flag:
        print("Generando resumen...")
        summary = generate_summary(transcription)
    
    # Paso 4: Guardar todo en un archivo
    content = f"TRANSCRIPCIÓN DE LA CLASE\n"
    content += f"{'=' * 80}\n\n"
    content += f"Archivo: {os.path.basename(video_path)}\n"
    content += f"Fecha de procesamiento: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    if summary:
        content += f"RESUMEN\n"
        content += f"{'-' * 80}\n"
        content += f"{summary}\n\n"
    
    content += f"TRANSCRIPCIÓN COMPLETA\n"
    content += f"{'-' * 80}\n"
    content += f"{transcription}\n"
    
    save_to_file(content, output_text_file)
    
    # Limpiar archivo de audio temporal
    if os.path.exists(audio_path):
        os.remove(audio_path)
        print(f"Archivo de audio temporal eliminado")
    
    return {
        'transcription': transcription,
        'summary': summary,
        'output_file': os.path.basename(output_text_file)
    }

if __name__ == "__main__":
    # Ejemplo de uso directo
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python transcriber.py <ruta_al_video.mp4>")
        sys.exit(1)
    
    video_file = sys.argv[1]
    
    if not os.path.exists(video_file):
        print(f"Error: El archivo {video_file} no existe")
        sys.exit(1)
    
    result = process_video(video_file, generate_summary_flag=True, model_size='base')
    print(f"\n✓ Proceso completado!")
    print(f"Archivo de salida: {result['output_file']}")
