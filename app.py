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
    "You are a virtual assistant designed to collect leads. Your goal is to collect the following information exactly once from the user:\n"
    "1. Full Name\n"
    "2. Email address or phone number\n"
    "3. Area of interest (e.g., web development, AI, marketing, etc.)\n\n"
    "Don't be too persistent with the information gathering, Be respectful to user's responses.\n"
    "Keep the conversation friendly and human-like. After collecting all the required details, thank the user and let them know that someone will reach out shortly.\n"
    "Do not respond to unrelated questions or entertain casual conversation beyond the lead collection task."
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
        cleaned_text = response.text.strip().replace("\n", "<br>")
        return jsonify({"reply": cleaned_text})

    except Exception:
        return jsonify({"reply": "Something went wrong, please try again."})

if __name__ == "__main__":
    app.run(debug=True)
