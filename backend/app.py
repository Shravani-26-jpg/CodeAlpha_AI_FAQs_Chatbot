from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

nltk.download("punkt")
nltk.download("stopwords")

STOPWORDS = set(stopwords.words("english"))

faqs = [
    {"question": "What is Artificial Intelligence?", "answer": "Artificial Intelligence is the ability of machines to perform tasks that normally require human intelligence."},
    {"question": "What is machine learning?", "answer": "Machine learning is a subset of AI that allows computers to learn from data without explicit programming."}
]

def clean_text(text):
    tokens = word_tokenize(text.lower())
    return " ".join([t for t in tokens if t not in STOPWORDS])

def load_faqs():
    for item in faqs:
        item["q_proc"] = clean_text(item["question"])
    return faqs

faqs = load_faqs()

@app.route("/chat", methods=["POST"])
def chat():
    user_q = request.json["question"]
    user_proc = clean_text(user_q)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([user_proc] + [f["q_proc"] for f in faqs])
    similarities = cosine_similarity(vectors[0:1], vectors[1:])
    best_index = similarities.argmax()

    return jsonify({"answer": faqs[best_index]["answer"]})

if __name__ == "__main__":
    app.run(debug=True)
