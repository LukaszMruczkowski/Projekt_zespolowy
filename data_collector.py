import requests
from bs4 import BeautifulSoup
import sqlite3

# Connect with database
connection = sqlite3.connect("words.db")

# Getting access to page that consists word lists devided by themes
urls_list = ["https://en.wikipedia.org/wiki/List_of_vegetables", "https://en.wikipedia.org/wiki/List_of_fish_common_names"]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


for url in urls_list:
    page = requests.get(url, headers=headers)

    # Object to scrape words
    soup = BeautifulSoup(page.content, "html.parser")

    # Find table tag
    table = soup.find('table')

    # Find all <a> tags with both href and title attributes
    a_tags = table.find_all('a', href=True, title=True)

    theme = url.split('/')[-1]

    # Create table
    cursor = connection.cursor()
    cursor.execute(f"CREATE TABLE if not exists {theme} (word TEXT);")

    # Insert words into table
    for tag in a_tags[1:]:
        print(tag.get_text())
        word = tag.get_text()
        if "'" in word:
            word = word.replace("'s", "")
        cursor.execute(f"INSERT INTO {theme} VALUES ('{word}');")

connection.commit()
connection.close()

