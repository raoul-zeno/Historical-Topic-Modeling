import pandas as pd
import unicodedata
import re
import sqlite3

con = sqlite3.connect("Database.db")
cur = con.cursor()

def preprocess_text(text):
    #lowercase the text
    result_text = text.lower()

    #normalize text
    result_text = unicodedata.normalize("NFD", result_text)

    #remove diaresis
    result_text = re.sub(r"(?<=\w)\u0364", "e", result_text)
    result_text = re.sub(r"o\u0308", "oe", result_text)
    result_text = re.sub(r"a\u0308", "ae", result_text)
    result_text = re.sub(r"u\u0308", "ue", result_text)

    #removing long s
    result_text = re.sub(r"\u017F", "s", result_text)

    #removing round r
    result_text = re.sub(r"\uA75B", "r", result_text)

    #removing ligatures
    result_text = re.sub(r"\u00E6", "ae", result_text)
    result_text = re.sub(r"\u0153", "oe", result_text)

    #removing abbreviations
    result_text = re.sub(r"m\u0303", "m", result_text)
    result_text = re.sub(r"n\u0303", "d", result_text)

    #remove unneeded special characters
    pattern = r"[/;:.,()\[\]\"\"*]"
    result_text = re.sub(pattern, "", result_text)

    #remove \n and -\n
    result_text = re.sub(r'- \n', "", result_text)
    result_text = re.sub(r'\n', '', result_text)

    #remove multiple spaces
    result_text = re.sub(" +", " ", result_text)

    #remove special characters
    result_text = re.sub(r"[^a-zA-Z\s]", "", result_text)

    #cleanup double spaces due to removal of single letters and digits
    result_text = re.sub(r"\s{2,}", " ", result_text).strip()

    return result_text
    
def add_pp_texts_to_database():
    number_of_entries = cur.execute("SELECT COUNT(*) FROM books").fetchone()
    for i in range(number_of_entries[0]):
        example_textObj = cur.execute("SELECT text FROM books WHERE text_index=?", (i,))
        example_text = example_textObj.fetchone()
        result_text = preprocess_text(example_text[0])
        cur.execute("UPDATE books SET preprocessed_text=? WHERE text_index=?", (result_text, i,))
    con.commit()












