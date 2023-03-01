FROM python:3.9

# Installe les paquets nécessaires pour l'accélération CPU
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libopenblas-dev

# Configure environnement variables for OpenBLAS
ENV OPENBLAS_NUM_THREADS=1
ENV OMP_NUM_THREADS=1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

# Install tesseract and its language files
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-deu vim

CMD ["python", "parking-access-mqtt-client.py"]
