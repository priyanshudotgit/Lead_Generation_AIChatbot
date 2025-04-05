from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure your Gemini API key
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Basic model with instructions
model = genai.GenerativeModel(
    model_name="gemini-2.5-pro-exp-03-25",
    system_instruction=(
        "You are a lead generation assistant. Collect the following info only once: "
        "1. Name, 2. Email or phone, 3. Area of interest.\n"
        "Talk like a human. Once info is collected, say thank you and stop asking further questions."
        "Do not entertain any other question (like jokes or anything other than collecting user's details)"
    )
)
chat = model.start_chat(history=[])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat_response():
    user_message = request.json.get("message")
    try:
        response = chat.send_message(user_message)
        return jsonify({"reply": response.text})
    except Exception:
        return jsonify({"reply": "Something went wrong, please try again."})

if __name__ == "__main__":
    app.run(debug=True)