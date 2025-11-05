FROM python:3.11-slim

# deps del sistema (para wheels básicos)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY main.py /app/

# instala nicegui
RUN pip install --no-cache-dir nicegui==1.* uvicorn

# Coolify / PaaS suelen inyectar PORT; respétalo si existe
ENV PORT=8080
EXPOSE 8080

CMD ["bash", "-lc", "python -u main.py --port ${PORT}"]
