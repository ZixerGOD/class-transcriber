import os
import sys
import zipfile
import urllib.request
import shutil

def install_ffmpeg():
    """Descarga e instala FFmpeg para Windows en la carpeta del proyecto"""
    
    ffmpeg_dir = os.path.join(os.getcwd(), 'ffmpeg')
    ffmpeg_bin = os.path.join(ffmpeg_dir, 'bin')
    ffmpeg_exe = os.path.join(ffmpeg_bin, 'ffmpeg.exe')
    
    # Verificar si ya está instalado
    if os.path.exists(ffmpeg_exe):
        print(f"FFmpeg ya está instalado en: {ffmpeg_exe}")
        print("Agregando al PATH del sistema...")
        os.environ['PATH'] = ffmpeg_bin + os.pathsep + os.environ['PATH']
        print("✓ FFmpeg configurado correctamente")
        return ffmpeg_exe
    
    print("Descargando FFmpeg...")
    url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    zip_path = "ffmpeg.zip"
    
    try:
        urllib.request.urlretrieve(url, zip_path)
        print("✓ Descarga completada")
        
        print("Extrayendo archivos...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('.')
        
        # Renombrar la carpeta extraída
        extracted_folder = None
        for item in os.listdir('.'):
            if item.startswith('ffmpeg-') and os.path.isdir(item):
                extracted_folder = item
                break
        
        if extracted_folder:
            if os.path.exists(ffmpeg_dir):
                shutil.rmtree(ffmpeg_dir)
            os.rename(extracted_folder, ffmpeg_dir)
            print(f"✓ FFmpeg instalado en: {ffmpeg_dir}")
        
        # Limpiar archivo zip
        os.remove(zip_path)
        
        # Agregar al PATH
        os.environ['PATH'] = ffmpeg_bin + os.pathsep + os.environ['PATH']
        
        print("\n✓ Instalación completada exitosamente!")
        print(f"FFmpeg ejecutable: {ffmpeg_exe}")
        print("\nNOTA: Debes agregar esta ruta al PATH de Windows de forma permanente:")
        print(f"  {ffmpeg_bin}")
        
        return ffmpeg_exe
        
    except Exception as e:
        print(f"✗ Error durante la instalación: {e}")
        return None

if __name__ == "__main__":
    install_ffmpeg()
