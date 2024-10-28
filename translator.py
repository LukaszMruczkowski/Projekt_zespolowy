import deepl
import sqlite3

auth_key = "ae890d15-3173-4e2f-bc36-90807286369c:fx"  # Replace with your key
translator = deepl.Translator(auth_key)

languages = ["FR", "ES", "CS", "DE", "PL"]

# Connect with database of words
words_conn = sqlite3.connect("words.db")

words_cursor = words_conn.cursor()

# This line for translating whole database
#tables = words_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

# Use this if you want to translate only chosen tables
tables = ["sports"]


# Do translation for every
for table in tables:
    # Create new database with translated words
    translated_words_conn = sqlite3.connect("translated_words_deepL.db")
    translated_words_cursor = translated_words_conn.cursor()
    # Create table
    translated_words_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table} (
    word TEXT PRIMARY KEY, 
    {languages[0]} TEXT, 
    {languages[1]} TEXT, 
    {languages[2]} TEXT, 
    {languages[3]} TEXT, 
    {languages[4]} TEXT)""")
    # Get rows of table
    words = words_cursor.execute(f"SELECT word FROM {table};")
    # Get word by word and translate it in 5 different languages
    for word in words:
        translated_words = [word[0]]
        for language in languages:
            translated_word = translator.translate_text(word[0], source_lang="EN", target_lang=language, context=table[0]) 
            translated_words.append(str(translated_word))
        print(f"TRANSLATED WORDS: {translated_words}\n")
        translated_words_cursor.execute(f"""INSERT OR IGNORE INTO {table} 
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
    
    
