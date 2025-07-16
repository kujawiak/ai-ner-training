import spacy
from spacy import displacy
import os
import sys

# --- Konfiguracja ---
# Upewnij się, że ta ścieżka wskazuje na folder z najlepszą wersją Twojego modelu.
MODEL_PATH = "model_wynikowy_cnn/model-last"
# --------------------


def test_model(model_path):
    """
    Główna funkcja do interaktywnego testowania modelu spaCy.
    """
    # Sprawdzenie, czy folder z modelem istnieje
    if not os.path.exists(model_path):
        print(f"BŁĄD: Nie znaleziono folderu z modelem w ścieżce: '{model_path}'")
        print("Upewnij się, że trening został zakończony i ścieżka jest poprawna.")
        return

    # Krok 1: Załadowanie wytrenowanego modelu
    print(f"Ładowanie modelu z '{model_path}'...")
    try:
        nlp = spacy.load(model_path)
        print("✔ Model załadowany pomyślnie.")
        print("Możesz teraz wpisywać tekst do analizy.")
        print("Aby zakończyć, wpisz 'wyjdz', 'exit' lub 'quit'.\n")
    except Exception as e:
        print(f"BŁĄD: Nie udało się załadować modelu. Problem: {e}")
        return

    # Krok 2: Pętla interaktywna
    while True:
        # Prośba o wprowadzenie tekstu przez użytkownika
        print("> Wpisz tekst (wieloliniowy, zakończ pustą linią):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        text = "\n".join(lines)

        # Warunek wyjścia z pętli
        if text.lower() in ["wyjdz", "exit", "quit"]:
            break
            
        if not text.strip():
            print("Wpisz jakiś tekst, aby go przeanalizować.")
            continue

        # Krok 3: Przetwarzanie tekstu przez model
        doc = nlp(text)

        # Krok 4: Prezentacja wyników
        print("\n--- Wyniki Predykcji ---")
        if not doc.ents:
            print("Nie znaleziono żadnych encji w podanym tekście.")
        else:
            # Opcja 1: Wizualizacja za pomocą displaCy (zalecane)
            # Wyświetla tekst z podświetlonymi encjami bezpośrednio w konsoli.
            displacy.render(doc, style="ent", jupyter=False)

            # Opcja 2: Prosty wydruk tekstowy (odkomentuj, jeśli chcesz go używać)
            print("\nLista znalezionych encji:")
            for ent in doc.ents:
                print(f"  - '{ent.text}' -> {ent.label_}")

        print("------------------------\n")

    print("Zakończono działanie programu.")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Interaktywne testowanie modelu spaCy.")
    parser.add_argument("model_path", nargs="?", default="models/test", help="Ścieżka do folderu z wytrenowanym modelem spaCy (domyślnie: models/test)")
    args = parser.parse_args()
    try:
        test_model(args.model_path)
    except KeyboardInterrupt:
        print("\nPrzerwano działanie programu.")