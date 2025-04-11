from flask import Flask, request, render_template, jsonify
import os
from gtts import gTTS
from playsound import playsound
import uuid

app = Flask(__name__)

def load_knowledge():
    knowledge = ""
    for filename in os.listdir("data"):
        if filename.endswith(".txt"):
            with open(os.path.join("data", filename), "r", encoding="utf-8") as f:
                knowledge += f.read() + "\n"
    return knowledge

knowledge_base = load_knowledge()

def speak_text(text, lang='en'):
    filename = f"temp_{uuid.uuid4()}.mp3"
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
    except Exception as e:
        print("Voice error:", e)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    response = "Here's what I found related to your question:\n\n" + knowledge_base[:500]
    lang = 'ar' if any(c in user_input for c in "ضصثقفغعهخحجدشسيبلاتنممكطئءؤرلاىةوزظ") else 'en'
    speak_text(response, lang=lang)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
