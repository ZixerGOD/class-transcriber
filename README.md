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

### Transcribir Videos

1. Ve a la pestaña "Transcribir Video"
2. Sube un archivo de video (MP4, AVI, MOV, MKV)
3. Espera a que se procese (esto puede tomar varios minutos dependiendo del tamaño del video)
4. Visualiza la transcripción y el resumen, o descarga el archivo de texto generado

### Humanizar Texto

1. Ve a la pestaña "Humanizar Texto"
2. Pega el texto que deseas mejorar (puede ser una transcripción o cualquier texto)
3. Haz clic en "Humanizar Texto"
4. Copia o guarda el resultado mejorado

### Resumir Texto

1. Ve a la pestaña "Resumir Texto"
2. Pega el texto largo que deseas resumir
3. Ajusta el porcentaje del resumen (10-70%)
4. Haz clic en "Resumir Texto"
5. Visualiza el resumen y las palabras clave extraídas

### Comprimir Medios

#### Comprimir Imagen
1. Ve a la pestaña "Comprimir Medios" → "Comprimir Imagen"
2. Selecciona una imagen
3. Ajusta la calidad (1-95%) y el ancho máximo
4. Haz clic en "Comprimir Imagen"
5. Descarga la imagen comprimida

#### Convertir Imagen
1. Ve a la pestaña "Comprimir Medios" → "Convertir Imagen"
2. Selecciona una imagen
3. Elige el formato de salida (WebP, JPG, PNG)
4. Ajusta la calidad
5. Haz clic en "Convertir Imagen"
6. Descarga la imagen convertida

#### Comprimir Video
1. Ve a la pestaña "Comprimir Medios" → "Comprimir Video"
2. Selecciona un video
3. Elige la calidad de salida (Baja, Media o Alta)
4. Haz clic en "Comprimir Video" (esto puede tomar varios minutos)
5. Descarga el video comprimido

## Características

- ✅ Extracción automática de audio desde videos
- ✅ Transcripción de audio a texto usando Whisper de OpenAI
- ✅ Generación de resúmenes automáticos
- ✅ Humanización de texto para mejorar legibilidad
- ✅ Resumen inteligente de textos largos con extracción de palabras clave
- ✅ Compresión de imágenes (reducir tamaño, píxeles, cambiar formato)
- ✅ Conversión de formatos de imagen (WebP, JPG, PNG)
- ✅ Compresión de videos (redimensionar, reducir bitrate)
- ✅ Interfaz web amigable con pestañas
- ✅ Descarga de resultados en formato texto

## Notas

- El procesamiento puede ser lento en CPU. Para mejor rendimiento, usa una GPU compatible con CUDA.
- Los archivos de video grandes pueden tomar mucho tiempo en procesarse.
- Los archivos procesados se guardan en la carpeta `outputs/`
