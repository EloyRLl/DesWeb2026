# Cambiamos a una base Debian-slim (más compatible con librerías GIS)
FROM python:3.12-slim

WORKDIR /usr/src/app

# Instalamos dependencias de sistema compatibles con Debian
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x entrypoint.sh
# Si tu initdb.sh no es estrictamente necesario para el inicio, 
# asegúrate de que no bloquee el contenedor.
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]