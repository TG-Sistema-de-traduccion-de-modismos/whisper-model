# **Whisper Model Service**

**Servicio de inferencia para transcripción de audio** usando **faster-whisper**.  
La imagen está optimizada para GPU **RTX 5070**. La imagen Docker resultante pesa aproximadamente **24.46 GB**.

## **Resumen**
Este repositorio solo carga **faster-whisper**, recibe archivos WAV y devuelve la transcripción. El servicio expone endpoints HTTP mínimos para comprobar estado y transcribir audio. Si faster-whisper no está disponible, el servicio registra una advertencia y entra en modo simulación.

> Nota: el servicio acepta exclusivamente archivos en formato **WAV**.

---

## **Características principales**
- Wrapper sobre **faster-whisper** para transcripción (solo WAV).  
- API ligera (FastAPI) con endpoints `/health` y `/transcribe`.  
- Imagen optimizada para **RTX 5070**.  
- Si no se empaqueta el modelo en la imagen, es recomendable montar la carpeta del modelo/cache con `-v` para evitar descargas repetidas.

---

## **Estructura del proyecto (resumen)**
- whisper-model/
  - Dockerfile
  - requirements.txt
  - .env (opcional)
  - app/
    - main.py
    - infrastructure/
      - routes.py
    - application/
      - model_wrapper.py
    - core/
      - config.py
      - logging_config.py
    - domain/
      - models.py 

---

## **Endpoints**
- **GET /health**  
  Retorna JSON con estado del servicio y disponibilidad del modelo.

- **POST /transcribe**  
  Espera un archivo WAV (multipart/form-data, campo `file`) y retorna la transcripción y metadatos (modelo usado, duración).

Ejemplo con curl:
```sh
curl -X POST http://localhost:8004/transcribe \
  -F "file=@audio.wav"
```

---

## **Docker — build & run (GPU, sin alternativa legacy)**
Requisitos en host: Docker 19.03+ y **NVIDIA Container Toolkit**.

1) Construir la imagen:
```sh
docker build -t whisper-service:latest ./whisper-model
```

2) Ejecutar (opción moderna, recomendada):
```sh
docker run --rm --name whisper-service `
  --gpus all `
  -e NVIDIA_VISIBLE_DEVICES=all `
  -e NVIDIA_DRIVER_CAPABILITIES=compute,utility `
  -p 8004:8004 `
  -v C:\ruta\al\audio:/app/audio `
  -v C:\ruta\al\modelo:/app/model `
  whisper-service:latest
```

Opciones útiles:
- `--shm-size=1g` si la app requiere más memoria compartida.  
- `-v <host_path>:/app/model` para montar modelos/cache y evitar descargas.

---

## **Configuración importante**
- Revisa `requirements.txt` y usa las versiones indicadas (p. ej. `faster-whisper`, `torch`).  
- Ajusta `MODEL_NAME` en `app/core/config.py` o `.env` para seleccionar el checkpoint a cargar.  
- Monta el directorio del modelo si no quieres incluirlo en la imagen.

---

## **Notas operativas**
- El wrapper (`app/application/model_wrapper.py`) carga `settings.MODEL_NAME` y, si `faster_whisper` no está disponible, opera en modo simulación (transcripción simulada).  
- Asegúrate de subir archivos en formato **WAV**; otros formatos no están soportados por este servicio.  
- Ejecutar en GPU con suficiente VRAM para evitar OOM con modelos grandes.  
- Revisar logs (logger) para diagnosticar errores de carga o transcripción.
