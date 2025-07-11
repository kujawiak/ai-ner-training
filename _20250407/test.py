print("1. Start skryptu testującego integrację")

try:
    import spacy
    # Ten import jest kluczowy - bez niego spaCy nie "zobaczy" transformera
    import spacy_transformers 
    print("2. Pomyślnie zaimportowano spaCy i spacy-transformers")

    # TEST 1: Sprawdzamy, czy spaCy "widzi" fabrykę komponentu 'transformer'
    # To jest to, co spacy.info() próbuje zrobić pod spodem.
    factory_name = "transformer"
    if spacy.Language.has_factory(factory_name):
        print(f"3. SUKCES! spaCy poprawnie rozpoznało fabrykę '{factory_name}'.")
    else:
        print(f"3. PORAŻKA! spaCy NIE WIDZI fabryki komponentu '{factory_name}'. To jest główny problem.")

    # TEST 2: Jeśli fabryka jest widoczna, próbujemy jej użyć
    if spacy.Language.has_factory(factory_name):
        print("4. Próba stworzenia potoku z komponentem 'transformer'...")
        try:
            nlp = spacy.blank("pl")
            nlp.add_pipe(factory_name)
            print("5. SUKCES! Pomyślnie dodano 'transformer' do potoku.")
        except Exception as e:
            print(f"5. PORAŻKA! Wystąpił błąd podczas dodawania komponentu do potoku: {e}")
            import traceback
            traceback.print_exc()

except Exception as e:
    print(f"\n!!!!!! WYSTĄPIŁ KRYTYCZNY BŁĄD PODCZAS IMPORTU LUB TESTU !!!!!!")
    print(f"Błąd: {e}")
    import traceback
    traceback.print_exc()

print("6. Koniec skryptu")