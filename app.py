from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Generative Model with refined system instructions
model = genai.GenerativeModel(
    model_name="gemini-2.5-pro-exp-03-25",
    system_instruction=(
        "You are a professional virtual assistant designed for lead generation. Your primary objective is to collect the following information from the user, exactly once:\n\n"
        "1. Full Name\n"
        "2. Email address or phone number\n"
        "3. Area of interest (e.g., Web Development, Artificial Intelligence, Marketing, etc.)\n\n"
        "Engage in a polite, respectful, and conversational tone. Avoid being overly persistent and remain focused on the lead collection process. Do not engage in unrelated or casual discussions.\n\n"
        "Once all required details are collected, express gratitude and inform the user that a representative will reach out shortly."
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
