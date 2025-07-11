import spacy
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from fastapi.responses import HTMLResponse
from fastapi import Request, Form
import html

# Domyślna ścieżka do modelu (możesz zmienić)
MODEL_PATH = "models/api_ner_model"

# Załaduj model NER przy starcie
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Nie znaleziono modelu w ścieżce: {MODEL_PATH}")
nlp = spacy.load(MODEL_PATH)

app = FastAPI()

class NERRequest(BaseModel):
    inputData: str

@app.post("/ner")
def ner_endpoint(request: NERRequest):
    # Zamień tekst na jedną linię
    clean_text = request.inputData.replace('\n', ' ').replace('\r', ' ')
    doc = nlp(clean_text)
    ents = [
        {
            "text": ent.text,
            "label": ent.label_,
            "start_char": ent.start_char,
            "end_char": ent.end_char
        }
        for ent in doc.ents
    ]
    return {"entities": ents}

@app.get("/ner", response_class=HTMLResponse)
def ner_form():
    return """
    <html>
        <head>
            <title>NER Demo</title>
        </head>
        <body>
            <h2>Demo rozpoznawania encji (NER)</h2>
            <form method="post" action="/ner_form">
                <textarea name="inputData" rows="6" cols="60" placeholder="Wpisz tekst tutaj..."></textarea><br>
                <button type="submit">Wyślij</button>
            </form>
        </body>
    </html>
    """

@app.post("/ner_form", response_class=HTMLResponse)
async def ner_form_post(request: Request, inputData: str = Form(...)):
    clean_text = inputData.replace('\n', ' ').replace('\r', ' ')
    doc = nlp(clean_text)
    ents = [
        {
            "text": ent.text,
            "label": ent.label_,
            "start_char": ent.start_char,
            "end_char": ent.end_char
        }
        for ent in doc.ents
    ]
    # Escape inputData for HTML
    safe_input = html.escape(inputData)
    ents_html = "<ul>" + "".join([f"<li><b>{html.escape(e['text'])}</b> ({e['label']}) [{e['start_char']}-{e['end_char']}]</li>" for e in ents]) + "</ul>" if ents else "<i>Brak encji</i>"
    return f"""
    <html>
        <head>
            <title>NER Demo - Wyniki</title>
        </head>
        <body>
            <h2>Demo rozpoznawania encji (NER)</h2>
            <form method="post" action="/ner_form">
                <textarea name="inputData" rows="6" cols="60">{safe_input}</textarea><br>
                <button type="submit">Wyślij</button>
            </form>
            <h3>Wynik:</h3>
            {ents_html}
            <br><a href="/ner">Wróć</a>
        </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run("ner_api:app", host="0.0.0.0", port=8099, reload=False)