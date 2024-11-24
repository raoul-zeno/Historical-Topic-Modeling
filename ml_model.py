import sqlite3
from bertopic import BERTopic
from cuml.cluster import HDBSCAN
from cuml.manifold import UMAP
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

con = sqlite3.connect("Database.db")
cur = con.cursor()

nltk.download("stopwords")

german_stop_words = stopwords.words("german")
vect = CountVectorizer(stop_words=german_stop_words)

def make_documents():
    documents = []
    range_index = cur.execute("SELECT COUNT(*) FROM my_data").fetchone()
    for i in range(range_index[0]):
        text = cur.execute("SELECT preprocessed_text FROM my_data WHERE text_index=?", (i,)).fetchone()
        documents.append(text[0])
    return documents

def train_model():
    documents = make_documents()
    # umap_model = UMAP(n_components=5, n_neighbors=15, min_dist=0.0)
    # hdbscan_model = HDBSCAN(min_samples=10, gen_min_span_tree=True, prediction_data=True)
    topic_model = BERTopic(language="multilingual", verbose=True, low_memory=True, vectorizer_model=vect)
    # embedding_model = "sentence-transformer/paraphrase-multilingual-MiniLM-L12-v2"
    # topic_model.save("C:/Users/RaoulZenoHub/OneDrive/Desktop", serialization="safetensors", save_ctfidf=True, save_embedding_model=embedding_model)
    topics, probs = topic_model.fit_transform(documents)
    topic_model.visualize_topics().show()

def main():
    train_model()

if __name__ == "__main__":
    main()