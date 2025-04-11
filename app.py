from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)

def load_knowledge():
    knowledge = ""
    for filename in os.listdir("data"):
        if filename.endswith(".txt"):
            with open(os.path.join("data", filename), "r", encoding="utf-8") as f:
                knowledge += f.read() + "\n"
    return knowledge

knowledge_base = load_knowledge()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]

    if "admission" in user_input.lower() or "القبول" in user_input:
        response = "Jazan University admission info can be found on the official site. شروط القبول يمكن العثور عليها في الموقع الرسمي."
    else:
        response = "Here's what I found related to your question:\n\n" + knowledge_base[:500]

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
