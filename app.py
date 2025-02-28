from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
API_TOKEN = os.getenv("HUGGING_FACE_TOKEN")  # Gets token from environment variable

def coffee_bot_response(user_input):
    user_input = user_input.strip().lower()
    
    # Call Hugging Face API
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {"inputs": user_input}
    response = requests.post(API_URL, headers=headers, json=payload)
    bot_reply = response.json()[0]["generated_text"] if response.ok else "Oops, something broke!"

    # Add coffee-specific logic
    if "coffee" in user_input or "latte" in user_input or "espresso" in user_input:
        bot_reply += " Ooh, coffee time! What kind? (latte, espresso, etc.)"
    elif any(x in user_input for x in ["latte", "espresso", "cappuccino"]):
        coffee_type = next(x for x in ["latte", "espresso", "cappuccino"] if x in user_input)
        bot_reply += f" Cool, a {coffee_type}! What size? (small, medium, large)"
    elif any(x in user_input for x in ["small", "medium", "large"]):
        size = next(x for x in ["small", "medium", "large"] if x in user_input)
        bot_reply += f" Your {size} coffee is brewing—enjoy!"
    elif "no" in user_input or "thanks" in user_input:
        bot_reply += " Enjoy your coffee! Come back anytime!"
    return bot_reply

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["message"]
        bot_reply = coffee_bot_response(user_input)
        return render_template("index.html", user_input=user_input, bot_reply=bot_reply)
    return render_template("index.html", user_input="", bot_reply="Hi! I’m Coffee Bot. Ready to brew something tasty?")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)