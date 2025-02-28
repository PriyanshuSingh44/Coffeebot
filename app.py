from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
API_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

def coffee_bot_response(user_input):
    user_input = user_input.strip().lower()
    
    # Add context for BlenderBot
    context = "You are a coffee-ordering bot with a sense of humor. Help the user order a coffee (e.g., latte, espresso, cappuccino) and ask for size if needed. Throw in some coffee puns or witty remarks!"
    full_input = f"{context} User says: {user_input}"

    # Call Hugging Face API
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {"inputs": full_input}
    response = requests.post(API_URL, headers=headers, json=payload)
    blender_reply = response.json()[0]["generated_text"] if response.ok else "Oops, I spilled the beans—something broke!"

    # Custom coffee logic with humor
    if "hi" in user_input or "hello" in user_input:
        bot_reply = "Hey there! I’m Coffee Bot, your barista with a brew-tiful personality. Name or coffee—what’s first?"
    elif "name is" in user_input:
        name = user_input.split("is")[-1].strip()
        bot_reply = f"Nice to meet you, {name}! What coffee’s gonna perk up your day? (latte, espresso, cappuccino)"
    elif any(x in user_input for x in ["latte", "espresso", "cappuccino"]):
        coffee_type = next(x for x in ["latte", "espresso", "cappuccino"] if x in user_input)
        if coffee_type == "latte":
            bot_reply = f"A latte? You’re milking this coffee thing! What size—small, medium, or large?"
        elif coffee_type == "espresso":
            bot_reply = f"Espresso? Shots fired! What size to fuel your buzz—small, medium, large?"
        elif coffee_type == "cappuccino":
            bot_reply = f"Cappuccino? Froth-tastic choice! Size it up—small, medium, large?"
    elif any(x in user_input for x in ["small", "medium", "large"]):
        size = next(x for x in ["small", "medium", "large"] if x in user_input)
        bot_reply = f"Your {size} coffee’s brewing faster than you can say ‘caffeine’! Anything else, or are we grounds for now?"
    elif "no" in user_input or "thanks" in user_input:
        bot_reply = "Enjoy your brew, you caffeine fiend! Come back when you need another jolt. ☕"
    else:
        bot_reply = blender_reply if response.ok else "Hmm, I’m stumped—grounds for a coffee order instead?"

    return bot_reply

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["message"]
        bot_reply = coffee_bot_response(user_input)
        return render_template("index.html", user_input=user_input, bot_reply=bot_reply)
    return render_template("index.html", user_input="", bot_reply="Hi! I’m Coffee Bot—here to brew some laughs and lattes. What’s up?")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)