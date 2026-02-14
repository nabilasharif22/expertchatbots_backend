from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
from dotenv import load_dotenv
import random

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Load multiple OpenAI API keys
API_KEYS = [
    os.getenv("OPENAI_API_KEY_1"),
    os.getenv("OPENAI_API_KEY_2")
]

# Filter out None keys
API_KEYS = [key for key in API_KEYS if key]

if not API_KEYS:
    raise ValueError("No OpenAI API keys found in environment variables.")

def get_openai_client():
    """Return a client using a random available API key (for failover)."""
    key = random.choice(API_KEYS)
    openai.api_key = key
    return openai

@app.route("/debate", methods=["POST"])
def debate():
    """
    Expects JSON: { "topic": str, "expert1": str, "expert2": str }
    Returns JSON:
    {
        "debate": "text of debate...",
        "figure": { "type": "bar", "labels": [...], "values": [...] }
    }
    """
    data = request.get_json()
    topic = data.get("topic")
    expert1 = data.get("expert1")
    expert2 = data.get("expert2")

    if not topic or not expert1 or not expert2:
        return jsonify({"error": "Missing topic or expert names"}), 400

    prompt = (
        f"Simulate a debate between {expert1} and {expert2} on the topic: \"{topic}\".\n\n"
        "Provide a few short back-and-forth exchanges separated by double newlines.\n"
        "Keep it concise but informative."
    )

    client = get_openai_client()

    try:
        response = client.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )

        debate_text = response.choices[0].message.content

        # Dummy figure data for chart
        figure_data = {
            "type": "bar",
            "labels": ["Supporting", "Opposing"],
            "values": [5, 3]
        }

        return jsonify({
            "debate": debate_text,
            "figure": figure_data
        })

    except openai.error.RateLimitError:
        # Try switching to the other key if available
        if len(API_KEYS) > 1:
            API_KEYS.reverse()  # simple failover
            return jsonify({"error": "Quota exceeded on first key. Please retry; backend switched API key."}), 429
        else:
            return jsonify({"error": "Quota exceeded. No alternative API keys available."}), 429

    except openai.error.OpenAIError as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
