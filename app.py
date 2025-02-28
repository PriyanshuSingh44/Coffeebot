from flask import Flask, render_template, request
import requests
import os 

app = Flask(__name__)


API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
API_TOKEN = os.getenv("HUGGING_FACE_TOKEN")


def coffee_bot_response(user_input):
    user_input = user_input.strip().lower()
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {"inputs": user_input}
    response = requests.post(API_URL, headers=headers, json=payload)
    bot_reply = response.json()[0]["generated_text"] if response.ok else "Oops, something broke!"

    # Add coffee-specific fun
    if "coffee" in user_input or "latte" in user_input or "espresso" in user_input:
        bot_reply += " Ooh, coffee time! What kind? (latte, espresso, etc.)"
    elif any(x in user_input for x in ["small", "medium", "large"]):
        size = next(x for x in ["small", "medium", "large"] if x in user_input)
        bot_reply += f" Your {size} coffee is brewing—enjoy!"
    return bot_reply
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["message"]
        bot_reply = coffee_bot_response(user_input)
        return render_template("index.html", user_input=user_input, bot_reply=bot_reply)
    return render_template("index.html", user_input="", bot_reply="")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)  # Change from debug mode