import sqlite3
from top2vec import Top2Vec

con = sqlite3.connect("Database.db")
cur = con.cursor()

def make_documents():
    documents = []
    range_index = cur.execute("SELECT COUNT(*) FROM books").fetchone()
    for i in range(range_index[0]):
        text = cur.execute("SELECT preprocessed_text FROM books WHERE text_index=?", (i,)).fetchone()
        documents.append(text[0])
    return documents

def train_model():
    documents = make_documents()
    test_model = Top2Vec(documents, speed="fast")
    return test_model
