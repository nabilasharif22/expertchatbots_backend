from dotenv import load_dotenv
load_dotenv()  # This reads the .env file automatically
import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI, OpenAIError

app = Flask(__name__)
CORS(app)

# Two OpenAI clients
llm_clients = [
    OpenAI(api_key=os.getenv("OPENAI_API_KEY")),        # Primary
    OpenAI(api_key=os.getenv("OPENAI_API_KEY_SECOND")) # Secondary
]

@app.route("/")
def home():
    return jsonify({"message": "Expert Chatbots Backend Running"})

@app.route("/debate", methods=["POST"])
def debate():
    data = request.get_json()
    topic = data.get("topic")
    expert1 = data.get("expert1")
    expert2 = data.get("expert2")

    if not topic or not expert1 or not expert2:
        return jsonify({"error": "Missing topic or expert names"}), 400

    prompt = (
        f'Simulate a debate between {expert1} and {expert2} on the topic: "{topic}".\n\n'
        'Each expert should:\n'
        '1. Give a short opening statement.\n'
        '2. Reference a numeric research finding (include a percentage or number).\n\n'
        'Keep each response under 150 words.'
    )

    debate_text = None

    # Try each API key in order
    for client in llm_clients:
        if client.api_key:  # Skip if key is None
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                debate_text = response.choices[0].message.content
                break  # Success! Stop trying other keys
            except OpenAIError as e:
                print(f"API key failed: {e}")
                continue  # Try next key

    # Fallback if all APIs fail
    if not debate_text:
        debate_text = f"Mock debate between {expert1} and {expert2} on {topic}."

    figure_data = {
        "type": "bar",
        "labels": ["Baseline", "Improved"],
        "values": [random.randint(50, 80), random.randint(60, 95)]
    }

    return jsonify({
        "topic": topic,
        "expert1": expert1,
        "expert2": expert2,
        "debate": debate_text,
        "figure": figure_data
    })

if __name__ == "__main__":
    app.run(debug=True)
