import spacy
from spacy import displacy
import os

# --- Konfiguracja ---
# Upewnij się, że ta ścieżka wskazuje na folder z najlepszą wersją Twojego modelu.
MODEL_PATH = "model_wynikowy_cnn/model-last"
# --------------------


def test_model():
    """
    Główna funkcja do interaktywnego testowania modelu spaCy.
    """
    # Sprawdzenie, czy folder z modelem istnieje
    if not os.path.exists(MODEL_PATH):
        print(f"BŁĄD: Nie znaleziono folderu z modelem w ścieżce: '{MODEL_PATH}'")
        print("Upewnij się, że trening został zakończony i ścieżka jest poprawna.")
        return

    # Krok 1: Załadowanie wytrenowanego modelu
    print(f"Ładowanie modelu z '{MODEL_PATH}'...")
    try:
        nlp = spacy.load(MODEL_PATH)
        print("✔ Model załadowany pomyślnie.")
        print("Możesz teraz wpisywać tekst do analizy.")
        print("Aby zakończyć, wpisz 'wyjdz', 'exit' lub 'quit'.\n")
    except Exception as e:
        print(f"BŁĄD: Nie udało się załadować modelu. Problem: {e}")
        return

    # Krok 2: Pętla interaktywna
    while True:
        # Prośba o wprowadzenie tekstu przez użytkownika
        text = input("> Wpisz tekst: ")

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
    try:
        test_model()
    except KeyboardInterrupt:
        print("\nPrzerwano działanie programu.")