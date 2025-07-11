import datetime
import random
import re
import string

def generate_text_with_placeholders(template_text: str, num_examples: int) -> list[str]:
    """
    Generuje wiele przykładów tekstu, zastępując różne symbole zastępcze.

    Args:
        template_text: Tekst wejściowy zawierający symbole zastępcze (np. "{DATA}", "{ART}", "{NUMER}", "{ROK}", "{NAZWA_USTAWY}").
        num_examples: Liczba przykładów do wygenerowania.

    Returns:
        Lista ciągów znaków, gdzie każdy ciąg jest przykładem z wypełnionymi symbolami.
    """
    generated_texts = []
    
    # Słownik do tłumaczenia miesięcy na polskie nazwy
    polish_months = {
        1: "stycznia", 2: "lutego", 3: "marca", 4: "kwietnia", 5: "maja", 6: "czerwca",
        7: "lipca", 8: "sierpnia", 9: "września", 10: "października", 11: "listopada", 12: "grudnia"
    }
    
     # Rozbudowana lista przykładowych nazw ustaw (100 pozycji) z poprawionym formatowaniem
    law_names = [
        "o transporcie drogowym",
        "o ruchu drogowym",
        "o prawach konsumenta",
        "o ochronie danych osobowych",
        "o systemie oświaty",
        "o rachunkowości",
        "o postępowaniu egzekucyjnym w administracji",
        "o systemie ubezpieczeń społecznych",
        "o cudzoziemcach",
        "o drogach publicznych",
        "o usługach turystycznych",
        "o działalności leczniczej",
        "o spółdzielniach mieszkaniowych",
        "o szkolnictwie wyższym i nauce",
        "o lasach",
        "o ochronie przyrody",
        "o rybołówstwie śródlądowym",
        "o sporcie",
        "o samorządzie gminnym",
        "o samorządzie powiatowym",
        "o samorządzie województwa",
        "o prawie autorskim i prawach pokrewnych",
        "o ochronie zwierząt",
        "o przeciwdziałaniu narkomanii",
        "o wychowaniu w trzeźwości i przeciwdziałaniu alkoholizmowi",
        "o powszechnym obowiązku obrony Rzeczypospolitej Polskiej",
        "o broni i amunicji",
        "o grach hazardowych",
        "o fundacjach",
        "o stowarzyszeniach",
        "o służbie cywilnej",
        "o policji",
        "o straży granicznej",
        "o straży pożarnej",
        "o komercjalizacji i prywatyzacji",
        "o zasadach nabywania nieruchomości przez cudzoziemców",
        "o odpadach",
        "o udostępnianiu informacji o środowisku i jego ochronie",
        "o charakterystyce energetycznej budynków",
        "o planowaniu i zagospodarowaniu przestrzennym",
        "o gospodarce nieruchomościami",
        "o własności lokali",
        "o księgach wieczystych i hipotece",
        "o notariacie",
        "– Prawo o adwokaturze",
        "– Prawo o prokuraturze",
        "– Prawo o ustroju sądów powszechnych",
        "o ewidencji ludności",
        "o dowodach osobistych",
        "o paszportach",
        "o prawach pacjenta i Rzeczniku Praw Pacjenta",
        "o świadczeniach opieki zdrowotnej finansowanych ze środków publicznych",
        "o systemie informacji w ochronie zdrowia",
        "o zwalczaniu chorób zakaźnych u zwierząt",
        "o systemie monitorowania i kontrolowania jakości paliw",
        "o biopaliwach i biokomponentach",
        "– Prawo geologiczne i górnicze",
        "o ochronie gruntów rolnych i leśnych",
        "o nawozach i nawożeniu",
        "o nasiennictwie",
        "o zwalczaniu chorób zakaźnych i zakażeń u ludzi",
        "o ochronie roślin",
        "o swobodzie działalności gospodarczej",
        "o cenach",
        "o informatyzacji działalności podmiotów realizujących zadania publiczne",
        "o usługach płatniczych",
        "o obrocie instrumentami finansowymi",
        "– Prawo bankowe",
        "o ubezpieczeniach obowiązkowych, Ubezpieczeniowym Funduszu Gwarancyjnym i Polskim Biurze Ubezpieczycieli Komunikacyjnych",
        "o działalności ubezpieczeniowej i reasekuracyjnej",
        "o ofercie publicznej i warunkach wprowadzania instrumentów finansowych do zorganizowanego systemu obrotu oraz o spółkach publicznych",
        "o nadzorze nad rynkiem finansowym",
        "o spółkach z ograniczoną odpowiedzialnością", # Uproszczone nazwy
        "o spółkach akcyjnych",
        "o odpowiedzialności podmiotów zbiorowych za czyny zabronione pod groźbą kary",
        "o dostępie do informacji publicznej",
        "o petycjach",
        "o kołach gospodyń wiejskich",
        "o ochronie dziedzictwa niematerialnego",
        "o zmianie niektórych ustaw w związku z przystąpieniem Rzeczypospolitej Polskiej do Unii Europejskiej",
        "o minimalnym wynagrodzeniu za pracę",
        "o związkach zawodowych",
        "o rozwiązywaniu sporów zbiorowych",
        "o czasie pracy kierowców",
        "o systemie identyfikacji i rejestracji zwierząt",
        "o Agencji Restrukturyzacji i Modernizacji Rolnictwa",
        "o Prawie wodnym",
        "o ochronie prawnej odmian roślin",
        "o ochronie zdrowia zwierząt oraz zwalczaniu chorób zakaźnych zwierząt",
        "o przeciwdziałaniu praniu pieniędzy oraz finansowaniu terroryzmu",
        "o Krajowym Rejestrze Sądowym",
        "o funduszach inwestycyjnych i zarządzaniu alternatywnymi funduszami inwestycyjnymi",
        "o obligacjach",
        "o listach zastawnych i bankach hipotecznych",
        "o działalności pocztowej",
        "– Prawo telekomunikacyjne",
        "o radiofonii i telewizji",
        "o kinematografii",
        "o muzeach",
        "o bibliotekach",
        "o organizowaniu i prowadzeniu działalności kulturalnej",
        "o systemie certyfikacji i nadzoru wyrobów budowlanych",
        "– Prawo budowlane",
        "o planowaniu rodziny, ochronie płodu ludzkiego i warunkach dopuszczalności przerywania ciąży",
        "o służbie medycyny pracy",
        "o Państwowej Inspekcji Pracy"
    ]
    
    current_year = datetime.date.today().year # Pobierz bieżący rok raz

    for _ in range(num_examples):
        current_text = template_text
        
        # --- Obsługa {DATA} ---
        data_matches = list(re.finditer(r"\{DATA\}", current_text))
        for match in data_matches:
            start_date = datetime.date.today() - datetime.timedelta(days=5*365)
            end_date = datetime.date.today() + datetime.timedelta(days=5*365)
            
            time_between_dates = end_date - start_date
            days_between_dates = time_between_dates.days
            random_number_of_days = random.randrange(days_between_dates)
            random_date = start_date + datetime.timedelta(days=random_number_of_days)
            
            day = random_date.day
            month_name = polish_months[random_date.month]
            year = random_date.year
            
            formatted_date = f"{day} {month_name} {year} r."
            current_text = re.sub(r"\{DATA\}", formatted_date, current_text, count=1)

        # --- Obsługa {ART} ---
        art_matches = list(re.finditer(r"\{ART\}", current_text))
        for match in art_matches:
            random_number = random.randint(1, 100)
            suffix = ""
            if random.random() < 0.5:
                suffix = random.choice(string.ascii_lowercase)
            
            formatted_art = f"{random_number}{suffix}"
            current_text = re.sub(r"\{ART\}", formatted_art, current_text, count=1)

        # --- Obsługa {NUMER} ---
        numer_matches = list(re.finditer(r"\{NUMER\}", current_text))
        for match in numer_matches:
            random_numeral = random.randint(1, 1200)
            formatted_numeral = str(random_numeral)
            current_text = re.sub(r"\{NUMER\}", formatted_numeral, current_text, count=1)

        # --- Obsługa {ROK} ---
        rok_matches = list(re.finditer(r"\{ROK\}", current_text))
        for match in rok_matches:
            random_year = random.randint(1960, current_year)
            formatted_year = str(random_year)
            current_text = re.sub(r"\{ROK\}", formatted_year, current_text, count=1)

        # --- Obsługa {NAZWA_USTAWY} ---
        # Znajdź wszystkie wystąpienia {NAZWA_USTAWY}
        nazwa_ustawy_matches = list(re.finditer(r"\{NAZWA_USTAWY\}", current_text))
        for match in nazwa_ustawy_matches:
            random_law_name = random.choice(law_names)
            current_text = re.sub(r"\{NAZWA_USTAWY\}", random_law_name, current_text, count=1)

        generated_texts.append(current_text)
        
    return generated_texts

# Przykład użycia:
if __name__ == "__main__":
    template = "Art. {ART}. W ustawie z dnia {DATA} {NAZWA_USTAWY} (Dz. U. z {ROK} r. poz. {NUMER}) wprowadza się następujące zmiany:"
    num_examples_to_generate = 15

    generated_output = generate_text_with_placeholders(template, num_examples_to_generate)

    for i, text in enumerate(generated_output):
        print(text)

    template = "Art. {ART}. W ustawie z dnia {DATA} {NAZWA_USTAWY} (Dz. U. poz. {NUMER}) wprowadza się następujące zmiany:"
    num_examples_to_generate = 15

    generated_output = generate_text_with_placeholders(template, num_examples_to_generate)

    for i, text in enumerate(generated_output):
        print(text)

    template = "Art. {ART}. W ustawie z dnia {DATA} {NAZWA_USTAWY} (Dz. U. z {ROK} r. poz. {NUMER}, oraz z {ROK} r. poz. {NUMER}, {NUMER} i {NUMER}) wprowadza się następujące zmiany:"
    num_examples_to_generate = 15

    generated_output = generate_text_with_placeholders(template, num_examples_to_generate)

    for i, text in enumerate(generated_output):
        print(text)
    
    template = "Art. {ART}. W ustawie z dnia {DATA} {NAZWA_USTAWY} (Dz. U. z {ROK} r. poz. {NUMER}, z {ROK} r. poz. {NUMER} oraz z {ROK} r. poz. {NUMER}) wprowadza się następujące zmiany:"
    num_examples_to_generate = 15

    generated_output = generate_text_with_placeholders(template, num_examples_to_generate)

    for i, text in enumerate(generated_output):
        print(text)