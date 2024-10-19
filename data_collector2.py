import requests
from bs4 import BeautifulSoup
import sqlite3

# Funkcja do tworzenia bazy danych SQLite i odpowiedniej tabeli na dany temat
def init_db(temat):
    conn = sqlite3.connect('words.db')  # Tworzy lub otwiera bazę danych slowa.db
    c = conn.cursor()
    # Tworzymy tabelę dla danego tematu z jedną kolumną 'word' (bez id)
    c.execute(f'''CREATE TABLE IF NOT EXISTS {temat} 
                  (word TEXT PRIMARY KEY)''')  # Tylko jedna kolumna 'word' jako klucz główny
    conn.commit()
    return conn

# Funkcja do scrapowania wyrazów z elementów o klasie 'wordlist-item'
def scrapuj(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Znajdujemy wszystkie elementy o klasie 'wordlist-item' w całej stronie
    wordlist_items = soup.find_all(class_='wordlist-item')

    slowa = []
    for item in wordlist_items:
        # Pobieramy tekst każdego elementu
        nazwa = item.text.strip()
        slowa.append(nazwa)

    return slowa  # Zwracamy listę wyrazów

# Funkcja do zapisywania danych do dynamicznie stworzonej tabeli
def zapisz_do_bazy(conn, temat, slowa):
    c = conn.cursor()
    for nazwa in slowa:  # Iterujemy tylko po nazwach
        c.execute(f'INSERT OR IGNORE INTO {temat} (word) VALUES (?)', (nazwa,))  # Wstawiamy do kolumny 'word'
    conn.commit()

# Funkcja do wypisania zawartości tabeli w bazie danych
def wypisz_z_bazy(conn, temat):
    c = conn.cursor()
    c.execute(f'SELECT * FROM {temat}')
    rows = c.fetchall()

    if rows:
        print(f"\nZawartość tabeli '{temat}':")
        for row in rows:
            print(f"Word: {row[0]}")  # Wypisujemy tylko słowo
    else:
        print(f"Tabela '{temat}' jest pusta.")

# Główna funkcja
def main():
    temat = "vegetables"
    url = "https://www.enchantedlearning.com/wordlist/vegetables.shtml"

    slowa = scrapuj(url)  # Scrapujemy dane z podanego URL

    if slowa:
        conn = init_db(temat)  # Tworzymy bazę danych i odpowiednią tabelę dla tematu
        zapisz_do_bazy(conn, temat, slowa)  # Zapisujemy dane do odpowiedniej tabeli
        wypisz_z_bazy(conn, temat)  # Wypisujemy zawartość tabeli
        conn.close()
        print(f'\nZapisano {len(slowa)} rekordów do tabeli "{temat}".')
    else:
        print(f'Nie znaleziono słów dla tematu "{temat}".')

if __name__ == '__main__':
    main()
