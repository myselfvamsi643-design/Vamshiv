
import os
from flask import Flask, jsonify, request, send_from_directory
from groq import Groq

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(
        os.path.dirname(os.path.abspath(__file__)),
        "index.html"
    )

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please type a question!"})

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return jsonify({"answer": "AI setup is incomplete."}), 500

    try:
        client = Groq(api_key=api_key)
        result = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are VAMSHIV AI, a helpful personal assistant. Answer clearly and simply."
                },
                {"role": "user", "content": question}
            ]
        )
        return jsonify({
            "answer": result.choices[0].message.content
        })
    except Exception:
        app.logger.exception("AI request failed")
        return jsonify({
            "answer": "AI connection failed. Please try again."
        }), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
  
