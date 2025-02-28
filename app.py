from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
API_TOKEN = os.getenv("HUGGING_FACE_TOKEN") #Hugging face API

def coffee_bot_response(user_input):
    user_input = user_input.strip().lower()
    
    # Add context to steer BlenderBot toward coffee
    context = "You are a coffee-ordering bot. Help the user order a coffee (e.g., latte, espresso, cappuccino) and ask for size if needed. Keep it fun!"
    full_input = f"{context} User says: {user_input}"

    # Call Hugging Face API
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {"inputs": full_input}
    print(f"API Token: {API_TOKEN}")
    response = requests.post(API_URL, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    # Get BlenderBot's reply or fallback
    blender_reply = response.json()[0]["generated_text"] if response.ok else "Oops, something broke!"

    # Custom coffee logic takes priority
    if "hi" in user_input or "hello" in user_input:
        bot_reply = "Hey there! I’m Coffee Bot. What’s your name or what coffee can I get started for you?"
    elif "name is" in user_input:
        name = user_input.split("is")[-1].strip()
        bot_reply = f"Nice to meet you, {name}! What coffee do you want? (latte, espresso, cappuccino)"
    elif any(x in user_input for x in ["latte", "espresso", "cappuccino"]):
        coffee_type = next(x for x in ["latte", "espresso", "cappuccino"] if x in user_input)
        bot_reply = f"Cool, a {coffee_type}! What size? (small, medium, large)"
    elif any(x in user_input for x in ["small", "medium", "large"]):
        size = next(x for x in ["small", "medium", "large"] if x in user_input)
        bot_reply = f"Your {size} coffee is brewing—enjoy! Anything else?"
    elif "no" in user_input or "thanks" in user_input:
        bot_reply = "Enjoy your coffee! Come back anytime!"
    else:
        # Use BlenderBot only for non-coffee chit-chat
        bot_reply = blender_reply if response.ok else "Hmm, not sure what you mean. Want a coffee?"

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