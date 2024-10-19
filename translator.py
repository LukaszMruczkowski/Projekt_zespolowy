from translate import Translator
import sqlite3

languages = ["fr", "hr", "cs", "de", "pl"]

# Connect with database of words
words_conn = sqlite3.connect("words.db")

words_cursor = words_conn.cursor()

tables = words_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

# Do translation for every
for table in tables:
    # Create new database with translated words
    translated_words_conn = sqlite3.connect("translated_words.db")
    translated_words_cursor = translated_words_conn.cursor()
    # Create table
    translated_words_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table[0]} (
    word TEXT PRIMARY KEY, 
    {languages[0]} TEXT, 
    {languages[1]} TEXT, 
    {languages[2]} TEXT, 
    {languages[3]} TEXT, 
    {languages[4]} TEXT)""")
    # Get rows of table
    words = words_cursor.execute(f"SELECT word FROM {table[0]};")
    # Get word by word and translate it in 5 different languages
    for word in words:
        translated_words = [word[0]]
        for language in languages:
            translator = Translator(language)
            translated_word = translator.translate(word[0])
            translated_words.append(translated_word)
        print(f"TRANSLATED WORDS: {translated_words}\n")
        translated_words_cursor.execute(f"""INSERT OR IGNORE INTO {table[0]} 
                                    (word, 
                                    {languages[0]}, 
                                    {languages[1]},
                                    {languages[2]}, 
                                    {languages[3]}, 
                                    {languages[4]}) 
                                    VALUES (?, ?, ?, ?, ?, ?)""",
                                (
                                    translated_words[0],
                                    translated_words[1],
                                    translated_words[2],
                                    translated_words[3],
                                    translated_words[4],
                                    translated_words[5]
                                ))
    translated_words_conn.commit()
# Close connections
words_conn.close()
translated_words_conn.close()
    
    
