FROM python:3-alpine3.22

WORKDIR /app

# Instalacja zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj plik ner_api.py
COPY ner_api.py .

# Skopiuj tylko katalog z modelem
COPY models/api_ner_model ./models/api_ner_model

# Domyślny port (można nadpisać przez zmienną środowiskową)
ENV PORT=5081

EXPOSE ${PORT}

CMD ["sh", "-c", "uvicorn ner_api:app --host 0.0.0.0 --port ${PORT}"]