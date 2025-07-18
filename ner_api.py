import spacy
from fastapi import FastAPI, Form, Request # Dodaj Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates # Dodaj Jinja2Templates
from pydantic import BaseModel
import uvicorn
import os
from typing import Optional, List

# --- Konfiguracja i ładowanie modeli ---

PT_MODEL_PATH = "models/api_ner_model"
TF_MODEL_PATH = "models/api_ner_model_tf"

if not os.path.exists(PT_MODEL_PATH):
    raise RuntimeError(f"Nie znaleziono modelu Tok2Vec w ścieżce: {PT_MODEL_PATH}")
if not os.path.exists(TF_MODEL_PATH):
    raise RuntimeError(f"Nie znaleziono modelu TensorFlow w ścieżce: {TF_MODEL_PATH}")

print(f"Ładowanie modelu Tok2Vec z '{PT_MODEL_PATH}'...")
nlp_pt = spacy.load(PT_MODEL_PATH)
print("Model Tok2Vec załadowany.")

print(f"Ładowanie modelu TensorFlow z '{TF_MODEL_PATH}'...")
nlp_tf = spacy.load(TF_MODEL_PATH)
print("Model TensorFlow załadowany.")

app = FastAPI(
    title="API do Rozpoznawania Encji Nazwanych (NER)",
    description="API oparte na FastAPI i spaCy do ekstrakcji encji z tekstu."
)

# Konfiguracja szablonów Jinja2
templates = Jinja2Templates(directory="templates")

# --- Modele danych (Pydantic) ---

class NERRequest(BaseModel):
    inputData: str

# --- Funkcje pomocnicze ---

def get_entities(text: str, model) -> list:
    """Przetwarza tekst za pomocą danego modelu spaCy i zwraca listę encji."""
    clean_text = text.replace('\n', ' ').replace('\r', ' ')
    doc = model(clean_text)
    return [
        {
            "text": ent.text,
            "label": ent.label_,
            "start_char": ent.start_char,
            "end_char": ent.end_char
        }
        for ent in doc.ents
    ]

# --- Endpoints API (zwracające JSON) - bez zmian ---

@app.post("/ner", summary="Przetwarzanie NER (model Tok2Vec)", tags=["API"])
def ner_endpoint(request: NERRequest):
    entities = get_entities(request.inputData, nlp_pt)
    return {"entities": entities, "model": "Tok2Vec"}

@app.post("/ner_tf", summary="Przetwarzanie NER (model TensorFlow)", tags=["API"])
def ner_tf_endpoint(request: NERRequest):
    entities = get_entities(request.inputData, nlp_tf)
    return {"entities": entities, "model": "TensorFlow"}

# --- Endpoints dla interfejsu HTML (ZMODYFIKOWANE) ---

@app.get("/ner_form", response_class=HTMLResponse, summary="Wyświetla formularz NER", tags=["Interfejs WWW"])
def ner_form(request: Request): # Musi przyjmować 'request'
    """Renderuje szablon HTML z pustym formularzem."""
    # Pierwszy argument to nazwa pliku, drugi to "kontekst" - słownik zmiennych dla szablonu
    return templates.TemplateResponse("ner_form.html", {"request": request})

@app.post("/ner/result", response_class=HTMLResponse, summary="Obsługuje formularz dla modelu Tok2Vec", tags=["Interfejs WWW"])
async def ner_form_result(request: Request, inputData: str = Form(...)):
    """Pobiera encje i renderuje ten sam szablon, ale z przekazanymi wynikami."""
    entities = get_entities(inputData, nlp_pt)
    context = {
        "request": request,
        "input_text": inputData,
        "entities": entities,
        "model_name": "Model Tok2Vec"
    }
    return templates.TemplateResponse("ner_form.html", context)

@app.post("/ner_tf/result", response_class=HTMLResponse, summary="Obsługuje formularz dla modelu TensorFlow", tags=["Interfejs WWW"])
async def ner_tf_form_result(request: Request, inputData: str = Form(...)):
    """Pobiera encje i renderuje ten sam szablon, ale z przekazanymi wynikami."""
    entities = get_entities(inputData, nlp_tf)
    context = {
        "request": request,
        "input_text": inputData,
        "entities": entities,
        "model_name": "Model TensorFlow"
    }
    return templates.TemplateResponse("ner_form.html", context)

# --- Uruchomienie aplikacji ---

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8099)