import sqlite3

con = sqlite3.connect("Database.db")
cur = con.cursor()

example_text = cur.execute("SELECT preprocessed_text FROM my_data WHERE text_index=4435").fetchone()

print(example_text[0])