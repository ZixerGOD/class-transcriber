import os
from PIL import Image
import subprocess
import json

def compress_image(input_path, output_path, quality=75, max_width=1920):
    """
    Comprime una imagen reduciendo calidad y redimensionando
    quality: 1-95 (menor = más comprimido)
    max_width: ancho máximo en píxeles
    """
    try:
        img = Image.open(input_path)
        
        # Redimensionar si es necesario
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Convertir a RGB si es necesario (para JPEG)
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        
        # Guardar con compresión
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        # Calcular cambio de tamaño
        original_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
        compressed_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
        compression_ratio = ((original_size - compressed_size) / original_size) * 100
        
        return {
            'success': True,
            'original_size': f"{original_size:.2f} MB",
            'compressed_size': f"{compressed_size:.2f} MB",
            'compression_ratio': f"{compression_ratio:.1f}%",
            'original_resolution': f"{img.width}x{img.height}"
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def convert_image_format(input_path, output_path, target_format='webp', quality=80):
    """
    Convierte imagen a otro formato (webp, png, jpg, etc)
    """
    try:
        img = Image.open(input_path)
        
        # Convertir a RGB si es necesario
        if img.mode in ('RGBA', 'LA') and target_format.lower() != 'png':
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        
        # Guardar en nuevo formato
        if target_format.lower() in ['jpg', 'jpeg']:
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
        elif target_format.lower() == 'webp':
            img.save(output_path, 'WEBP', quality=quality)
        else:
            img.save(output_path, target_format.upper())
        
        # Calcular cambio de tamaño
        original_size = os.path.getsize(input_path) / (1024 * 1024)
        converted_size = os.path.getsize(output_path) / (1024 * 1024)
        compression_ratio = ((original_size - converted_size) / original_size) * 100
        
        return {
            'success': True,
            'original_size': f"{original_size:.2f} MB",
            'converted_size': f"{converted_size:.2f} MB",
            'compression_ratio': f"{compression_ratio:.1f}%",
            'format': target_format.upper()
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def compress_video(input_path, output_path, quality='medium'):
    """
    Comprime un video reduciendo bitrate y resolución
    quality: 'low' (360p), 'medium' (480p), 'high' (720p), 'very_high' (1080p)
    """
    try:
        # Configurar parámetros según calidad
        quality_settings = {
            'low': {
                'width': 640,
                'height': 360,
                'bitrate': '500k',
                'crf': 28
            },
            'medium': {
                'width': 854,
                'height': 480,
                'bitrate': '1500k',
                'crf': 25
            },
            'high': {
                'width': 1280,
                'height': 720,
                'bitrate': '2500k',
                'crf': 23
            },
            'very_high': {
                'width': 1920,
                'height': 1080,
                'bitrate': '5000k',
                'crf': 18
            }
        }
        
        settings = quality_settings.get(quality, quality_settings['medium'])
        
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-vf', f"scale={settings['width']}:{settings['height']}",
            '-b:v', settings['bitrate'],
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-crf', str(settings['crf']),
            '-c:a', 'aac',
            '-b:a', '128k',
            '-y',
            output_path
        ]
        
        print(f"Ejecutando comando FFmpeg: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)  # 10 minutos de timeout
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Video compression timed out (exceeded 10 minutes)'}
        
        if result.returncode != 0:
            print(f"Error FFmpeg (código {result.returncode}):")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return {'success': False, 'error': f'FFmpeg error: {result.stderr}'}
        
        # Calcular cambio de tamaño
        if not os.path.exists(output_path):
            return {'success': False, 'error': 'Output file was not created'}
        
        original_size = os.path.getsize(input_path) / (1024 * 1024)
        compressed_size = os.path.getsize(output_path) / (1024 * 1024)
        
        if original_size == 0:
            compression_ratio = 0
        else:
            compression_ratio = ((original_size - compressed_size) / original_size) * 100
        
        return {
            'success': True,
            'original_size': f"{original_size:.2f} MB",
            'compressed_size': f"{compressed_size:.2f} MB",
            'compression_ratio': f"{compression_ratio:.1f}%",
            'quality': quality,
            'resolution': f"{settings['width']}x{settings['height']}"
        }
    except Exception as e:
        print(f"Exception in compress_video: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}

def convert_video_format(input_path, output_path, target_format='mp4'):
    """
    Convierte un video a otro formato
    target_format: 'mp4', 'mov', 'avi', 'mkv', 'webm', 'flv'
    """
    try:
        # Mapeo de formatos a códecs
        format_settings = {
            'mp4': {
                'vcodec': 'libx264',
                'acodec': 'aac',
                'preset': 'ultrafast'
            },
            'mov': {
                'vcodec': 'libx264',
                'acodec': 'aac',
                'preset': 'ultrafast'
            },
            'avi': {
                'vcodec': 'mpeg4',
                'acodec': 'libmp3lame',
                'preset': 'ultrafast'
            },
            'mkv': {
                'vcodec': 'libx264',
                'acodec': 'aac',
                'preset': 'ultrafast'
            },
            'webm': {
                'vcodec': 'libvpx-vp9',
                'acodec': 'libopus',
                'preset': 'ultrafast'
            },
            'flv': {
                'vcodec': 'mpeg4',
                'acodec': 'libmp3lame',
                'preset': 'ultrafast'
            }
        }
        
        settings = format_settings.get(target_format.lower(), format_settings['mp4'])
        
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-c:v', settings['vcodec'],
            '-c:a', settings['acodec'],
            '-preset', settings['preset'],
            '-b:a', '192k',
            '-y',
            output_path
        ]
        
        print(f"Ejecutando comando FFmpeg para conversión: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)  # 15 minutos de timeout
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Video conversion timed out (exceeded 15 minutes)'}
        
        if result.returncode != 0:
            print(f"Error FFmpeg (código {result.returncode}):")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return {'success': False, 'error': f'FFmpeg error: {result.stderr}'}
        
        # Calcular cambio de tamaño
        if not os.path.exists(output_path):
            return {'success': False, 'error': 'Output file was not created'}
        
        original_size = os.path.getsize(input_path) / (1024 * 1024)
        converted_size = os.path.getsize(output_path) / (1024 * 1024)
        
        if original_size == 0:
            compression_ratio = 0
        else:
            compression_ratio = ((original_size - converted_size) / original_size) * 100
        
        return {
            'success': True,
            'original_size': f"{original_size:.2f} MB",
            'converted_size': f"{converted_size:.2f} MB",
            'compression_ratio': f"{compression_ratio:.1f}%",
            'format': target_format.upper()
        }
    except Exception as e:
        print(f"Exception in convert_video_format: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}

def get_media_info(file_path):
    """
    Obtiene información sobre un archivo multimedia
    """
    try:
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']:
            img = Image.open(file_path)
            return {
                'type': 'image',
                'size': f"{file_size:.2f} MB",
                'format': file_ext[1:].upper(),
                'resolution': f"{img.width}x{img.height}",
                'mode': img.mode
            }
        elif file_ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']:
            # Para videos, usar ffprobe
            cmd = ['ffprobe', '-v', 'error', '-print_format', 'json', 
                   '-show_format', '-show_streams', file_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            info = json.loads(result.stdout)
            
            duration = float(info['format'].get('duration', 0))
            video_stream = next((s for s in info['streams'] if s['codec_type'] == 'video'), None)
            
            return {
                'type': 'video',
                'size': f"{file_size:.2f} MB",
                'format': file_ext[1:].upper(),
                'duration': f"{duration/60:.1f} minutes",
                'resolution': f"{video_stream['width']}x{video_stream['height']}" if video_stream else 'Unknown',
                'codec': video_stream['codec_name'] if video_stream else 'Unknown'
            }
    except:
        return {'error': 'No se pudo obtener información del archivo'}

if __name__ == "__main__":
    print("Módulo de compresión de medios cargado correctamente")
