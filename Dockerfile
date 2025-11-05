# Dockerfile (en la raíz del repo)
FROM python:3.11-slim

# paquetes básicos para compilar ruedas si alguna lib lo pide
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
# copia tu app
COPY main.py /app/

# 🔽 AQUI va la línea que preguntas (instala dependencias)
RUN pip install --no-cache-dir nicegui==1.* uvicorn SQLAlchemy psycopg[binary]

# puerto interno de la app
ENV PORT=8080
EXPOSE 8080

# arranque
CMD ["bash", "-lc", "python -u main.py --port ${PORT}"]
