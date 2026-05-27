from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)

# Enable CORS for frontend development
CORS(app, resources={r"/*": {"origins": "*"}})

# Positive and Negative keyword lists
positive_words = [
    "great", "amazing", "excellent", "love", "good", "awesome", "fantastic", "best",
    "outstanding", "superb", "brilliant", "perfect", "wonderful", "exceptional",
    "incredible", "recommend", "beautiful", "stunning", "masterpiece"
]

negative_words = [
    "bad", "terrible", "awful", "hate", "worst", "boring", "poor", "disappointing",
    "horrible", "dreadful", "useless", "waste", "mediocre", "pathetic", "disgusting",
    "avoid", "terrible", "rushed", "disappointed", "overrated"
]


def predict_sentiment(text):
    if not text or not text.strip():
        return {
            "sentiment": "Neutral",
            "confidence": 65,
            "scores": {"positive": 25, "negative": 25, "neutral": 40, "mixed": 10},
            "insight": "No meaningful text was provided for analysis."
        }

    words = text.lower().split()
    pos_count = sum(1 for w in words if w.strip() in positive_words)
    neg_count = sum(1 for w in words if w.strip() in negative_words)

    total_emotional = pos_count + neg_count

    if pos_count > neg_count and total_emotional > 0:
        sentiment = "Positive"
        scores = {"positive": 78, "negative": 7, "neutral": 8, "mixed": 7}
        confidence = random.randint(86, 97)
        insight = "Strong positive language and enthusiastic tone detected."

    elif neg_count > pos_count and total_emotional > 0:
        sentiment = "Negative"
        scores = {"positive": 7, "negative": 78, "neutral": 8, "mixed": 7}
        confidence = random.randint(84, 95)
        insight = "Negative words and critical tone strongly influenced the result."

    elif pos_count > 0 and neg_count > 0:
        sentiment = "Mixed"
        scores = {"positive": 42, "negative": 42, "neutral": 8, "mixed": 8}
        confidence = random.randint(73, 89)
        insight = "Both positive and negative sentiments were detected in the text."

    else:
        sentiment = "Neutral"
        scores = {"positive": 22, "negative": 18, "neutral": 52, "mixed": 8}
        confidence = random.randint(70, 83)
        insight = "The text shows low emotional intensity, resulting in neutral sentiment."

    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "scores": scores,
        "insight": insight
    }


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True)
    
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400
    
    result = predict_sentiment(data["text"])
    return jsonify(result)


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "Flask Sentiment Analysis Backend is running",
        "port": 5000,
        "endpoint": "/analyze"
    })


if __name__ == "__main__":
    print("Sentiment Analysis Server")
    app.run(debug=True, port=5000, host='0.0.0.0')