import sqlite3
import pandas as pd

db_file = 'translated_words_deepL.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    columns = [description[0] for description in cursor.description]

    df = pd.DataFrame(rows, columns=columns)

    csv_file = f"{table_name}.csv"
    df.to_csv(csv_file, index=False)

    print(f"Table {table_name} exported to {csv_file}")

conn.close()
