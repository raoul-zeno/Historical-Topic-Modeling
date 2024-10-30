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
    model = Top2Vec(documents=documents, embedding_model="universal-sentence-encoder-multilingual", speed="fast")
    return model

model = train_model()
model.save("firstmodel")

topic_sizes, topic_num = model.get_topic_sizes()
print("Number of topics: ", len(topic_sizes))

topic_words, word_scores, topic_scores, topic_nums = model.get_topics()

print("Top words in the first topic are: ", topic_words[0])