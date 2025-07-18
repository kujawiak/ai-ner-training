FROM python:3.13-slim
RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

# Instalacja zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ner_api.py .
COPY templates/ templates/

# Skopiuj tylko katalog z modelem
#COPY models/api_ner_model ./models/api_ner_model
#COPY models/api_ner_model_tf ./models/api_ner_model_tf

# Domyślny port (można nadpisać przez zmienną środowiskową)
ENV PORT=5081

EXPOSE ${PORT}

CMD ["sh", "-c", "uvicorn ner_api:app --host 0.0.0.0 --port ${PORT}"]