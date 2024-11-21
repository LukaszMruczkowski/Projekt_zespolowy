import requests
from bs4 import BeautifulSoup
import csv
import os

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
def zapisz_do_folderu(temat, slowa):
    print(os.getcwd())
    path = rf"{os.getcwd()}/words"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(rf"{path}/{temat}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows([slowa])
    

# Główna funkcja
def main():
    urls = ["https://www.enchantedlearning.com/wordlist/vegetables.shtml",
    "https://www.enchantedlearning.com/wordlist/animal.shtml",
    "https://www.enchantedlearning.com/wordlist/body.shtml",
    "https://www.enchantedlearning.com/wordlist/buildings.shtml",
    "https://www.enchantedlearning.com/wordlist/carparts.shtml",
    "https://www.enchantedlearning.com/wordlist/colors.shtml",
    "https://www.enchantedlearning.com/wordlist/computer.shtml",
    "https://www.enchantedlearning.com/wordlist/furniture.shtml",
    "https://www.enchantedlearning.com/wordlist/food.shtml",
    "https://www.enchantedlearning.com/wordlist/insect.shtml",
    "https://www.enchantedlearning.com/wordlist/landforms.shtml",
    "https://www.enchantedlearning.com/wordlist/military.shtml",
    "https://www.enchantedlearning.com/wordlist/sports.shtml",
    "https://www.enchantedlearning.com/wordlist/vegetables.shtml",
    "https://www.enchantedlearning.com/wordlist/transportation.shtml",
    "https://www.enchantedlearning.com/wordlist/vacation.shtml",
    "https://www.enchantedlearning.com/wordlist/flowers.shtml",
    "https://enchantedlearning.com/wordlist/family.shtml",
    "https://www.enchantedlearning.com/wordlist/container.shtml",
    "https://www.enchantedlearning.com/wordlist/clothes.shtml",
    "https://www.enchantedlearning.com/wordlist/birds.shtml"
    ]

    for url in urls:
        topic = url.split(r"/")[-1].split('.')[0]

        slowa = scrapuj(url)  # Scrapujemy dane z podanego URL

        if slowa:
            zapisz_do_folderu(topic, slowa)  # Zapisujemy dane do odpowiedniej tabeli
            print(f'\nZapisano {len(slowa)} rekordów do tabeli "{topic}".')
        else:
            print(f'Nie znaleziono słów dla tematu "{topic}".')

if __name__ == '__main__':
    main()
