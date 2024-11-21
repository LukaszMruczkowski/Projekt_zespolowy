import deepl
import os
import csv

auth_key = "ae890d15-3173-4e2f-bc36-90807286369c:fx"  # Replace with your key
translator = deepl.Translator(auth_key)

languages = ["FR", "ES", "CS", "DE", "PL"]

# List all topics based on CSV files in the "words" directory
topics = [os.path.splitext(name)[0] for name in os.listdir("./words") if name.endswith(".csv")]
topic = topics[20]
#for topic in topics:
input_file_path = f"./words/{topic}.csv"
output_file_path = f"./translated_words/{topic}_translated.csv"

# Ensure the output directory exists
os.makedirs("./translated_words", exist_ok=True)

with open(input_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    words = [row for row in reader]  # Assumes each row contains one word
    
# Prepare the output structure
translated_words = []
for word in words[0]:
    translation_row = {"EN": word}
    for language in languages:
        translated_word = translator.translate_text(word, source_lang="EN", target_lang=language).text
        translation_row[language] = translated_word
    translated_words.append(translation_row)
    print(f"Translated '{word}' into {translation_row}")

    # Write the translated words to a new CSV
    with open(output_file_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["EN"] + languages)
        writer.writeheader()
        writer.writerows(translated_words)

    print(f"Translated words for topic '{topic}' saved to {output_file_path}.")
