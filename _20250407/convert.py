import spacy
from spacy.tokens import DocBin
from spacy.util import load_model_from_config
from thinc.api import Config
import json
import warnings
import random

# --- Konfiguracja ---
CONFIG_PATH = "config_cnn.cfg"
INPUT_FILE = "all.jsonl"  # Twój główny plik z wszystkimi danymi
TRAIN_OUTPUT_FILE = "trening.spacy"
DEV_OUTPUT_FILE = "dev.spacy"
SPLIT_RATIO = 0.8  # 80% na trening, 20% na deweloperski
# --------------------

# Wczytaj konfigurację spaCy, aby użyć tego samego tokenizera
print(f"Ładowanie konfiguracji z {CONFIG_PATH}...")
config = Config().from_disk(CONFIG_PATH)
nlp = spacy.util.load_model_from_config(config, auto_fill=True)
print("Pomyślnie załadowano potok nlp.")

# Wczytaj wszystkie dane do pamięci
print(f"Wczytywanie danych z {INPUT_FILE}...")
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    all_data = [json.loads(line) for line in f]
print(f"Wczytano {len(all_data)} dokumentów.")

# Wymieszaj dane losowo - to kluczowy krok dla dobrego podziału!
random.shuffle(all_data)
print("Dane zostały losowo wymieszane.")

# Podziel dane na zbiór treningowy i deweloperski
split_point = int(len(all_data) * SPLIT_RATIO)
train_data = all_data[:split_point]
dev_data = all_data[split_point:]
print(f"Podział danych -> Trening: {len(train_data)}, Deweloperski: {len(dev_data)}")

# Funkcja pomocnicza do tworzenia obiektów DocBin, aby uniknąć powtarzania kodu
def create_doc_bin(data, nlp_pipeline):
    db = DocBin()
    for entry in data:
        text = entry.get('text', '')
        doc = nlp_pipeline.make_doc(text)
        ents = []
        for entity in entry.get('entities', []):
            start = entity['start_offset']
            end = entity['end_offset']
            label = entity['label']
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                msg = (
                    f"Pominięto encję, ponieważ jej granice [{start}, {end}, '{label}'] "
                    f"nie pasują do granic tokenów w tekście: '{text}'"
                )
                warnings.warn(msg)
            else:
                ents.append(span)
        try:
            doc.ents = ents
            db.add(doc)
        except ValueError as e:
            warnings.warn(f"Błąd podczas ustawiania encji dla tekstu: '{text}'. Błąd: {e}")
    return db

# Przetwarzanie i zapis zbioru treningowego
print("\nPrzetwarzanie zbioru treningowego...")
train_db = create_doc_bin(train_data, nlp)
train_db.to_disk(TRAIN_OUTPUT_FILE)
print(f"Zapisano zbiór treningowy w pliku: {TRAIN_OUTPUT_FILE}")

# Przetwarzanie i zapis zbioru deweloperskiego
print("\nPrzetwarzanie zbioru deweloperskiego...")
dev_db = create_doc_bin(dev_data, nlp)
dev_db.to_disk(DEV_OUTPUT_FILE)
print(f"Zapisano zbiór deweloperski w pliku: {DEV_OUTPUT_FILE}")

print("\nKonwersja zakończona sukcesem!")