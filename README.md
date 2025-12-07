# Class Transcriber

Aplicación web para transcribir y resumir clases en video (MP4, AVI, MOV, MKV).

## Requisitos

### FFmpeg
Este proyecto requiere FFmpeg instalado en tu sistema.

#### Opción 1: Instalar con Chocolatey (Recomendado)
1. Abre PowerShell como Administrador
2. Ejecuta:
```powershell
choco install ffmpeg -y
```

#### Opción 2: Instalación Manual
1. Descarga FFmpeg desde: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
2. Extrae el archivo ZIP
3. Copia la carpeta `bin` a `C:\ffmpeg\bin`
4. Agrega `C:\ffmpeg\bin` al PATH de Windows:
   - Busca "Variables de entorno" en el menú de Windows
   - En "Variables del sistema", selecciona "Path" y haz clic en "Editar"
   - Haz clic en "Nuevo" y agrega: `C:\ffmpeg\bin`
   - Haz clic en "Aceptar" en todas las ventanas

5. Verifica la instalación abriendo una nueva ventana de PowerShell y ejecutando:
```powershell
ffmpeg -version
```

## Instalación del Proyecto

1. Clona o descarga este repositorio
2. Crea un entorno virtual:
```powershell
python -m venv .venv
```

3. Activa el entorno virtual:
```powershell
.\.venv\Scripts\Activate.ps1
```

4. Instala las dependencias:
```powershell
pip install flask moviepy openai-whisper torch werkzeug imageio-ffmpeg
```

## Uso

1. Inicia el servidor:
```powershell
python app.py
```

2. Abre tu navegador en: `http://localhost:5000`

3. Sube un archivo de video (MP4, AVI, MOV, MKV)

4. Espera a que se procese (esto puede tomar varios minutos dependiendo del tamaño del video)

5. Visualiza la transcripción y el resumen, o descarga el archivo de texto generado

## Características

- ✅ Extracción automática de audio desde videos
- ✅ Transcripción de audio a texto usando Whisper de OpenAI
- ✅ Generación de resúmenes automáticos
- ✅ Interfaz web amigable
- ✅ Descarga de resultados en formato texto

## Notas

- El procesamiento puede ser lento en CPU. Para mejor rendimiento, usa una GPU compatible con CUDA.
- Los archivos de video grandes pueden tomar mucho tiempo en procesarse.
- Los archivos procesados se guardan en la carpeta `outputs/`
