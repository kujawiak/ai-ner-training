import spacy
from spacy.tokens import DocBin
from spacy.util import load_model_from_config
from thinc.api import Config
import json
import warnings
import random
import argparse # Krok 1: Import nowej biblioteki
import os

# --- Konfiguracja (część stała) ---
INPUT_FILE = "all.jsonl"
TRAIN_OUTPUT_FILE = "trening.spacy"
DEV_OUTPUT_FILE = "dev.spacy"
SPLIT_RATIO = 0.8
# --------------------

def create_doc_bin(data, nlp_pipeline):
    """Funkcja pomocnicza do tworzenia obiektów DocBin."""
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

def main(config_path, input_file):
    config_path = os.path.join("config", config_path)
    input_file = os.path.join("datasets", input_file)
    # Wczytaj konfigurację spaCy z podanej ścieżki
    print(f"Ładowanie konfiguracji z {config_path}...")
    try:
        config = Config().from_disk(config_path)
        nlp = spacy.util.load_model_from_config(config, auto_fill=True)
        print("Pomyślnie załadowano potok nlp.")
    except FileNotFoundError:
        print(f"BŁĄD: Plik konfiguracyjny nie został znaleziony w ścieżce: '{config_path}'")
        return

    # Wczytaj wszystkie dane do pamięci
    print(f"Wczytywanie danych z {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        all_data = [json.loads(line) for line in f]
    print(f"Wczytano {len(all_data)} dokumentów.")

    # Wymieszaj i podziel dane
    random.shuffle(all_data)
    split_point = int(len(all_data) * SPLIT_RATIO)
    train_data = all_data[:split_point]
    dev_data = all_data[split_point:]
    print(f"Podział danych -> Trening: {len(train_data)}, Deweloperski: {len(dev_data)}")

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


# Krok 2: Logika do obsługi argumentów wiersza poleceń
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Konwertuje dane z JSONL do formatu .spacy i dzieli je na zbiór treningowy i deweloperski.")
    parser.add_argument("config_path", nargs="?", default="cnn.cfg", help="Ścieżka do pliku konfiguracyjnego spaCy (.cfg) (domyślnie: cnn.cfg)")
    parser.add_argument("input_file", nargs="?", default=INPUT_FILE, help="Ścieżka do pliku wejściowego JSONL (domyślnie: all.jsonl)")
    args = parser.parse_args()
    main(args.config_path, args.input_file)