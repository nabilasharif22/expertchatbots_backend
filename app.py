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

def generate_expert_response(client, expert_name, topic, conversation_history, is_opening=False):
    """Generate a single expert's response based on conversation history."""
    if is_opening:
        system_prompt = f"You are {expert_name}, engaging in a natural conversation about {topic}. Start with a brief, conversational opening statement (2-3 sentences). Be personable and authentic, not overly formal. Share your perspective naturally."
    else:
        system_prompt = f"You are {expert_name}, continuing a conversation about {topic}. Respond naturally to what was just said. Be conversational, ask questions, acknowledge points, and share insights. Keep it to 2-3 sentences. Sound human, not like a debate robot."
    
    messages = [{"role": "system", "content": system_prompt}] + conversation_history
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.8,
            max_tokens=150
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        print(f"API error: {e}")
        return None

@app.route("/debate", methods=["POST"])
def debate():
    data = request.get_json()
    topic = data.get("topic")
    expert1 = data.get("expert1")
    expert2 = data.get("expert2")
    turns = data.get("turns", 3)  # Number of back-and-forth exchanges

    if not topic or not expert1 or not expert2:
        return jsonify({"error": "Missing topic or expert names"}), 400

    # Initialize conversation history
    conversation_history = [
        {"role": "user", "content": f"You're having a casual conversation about {topic}. Share your thoughts naturally."}
    ]
    
    debate_exchanges = []
    
    # Try each API key until one works
    working_client = None
    for client in llm_clients:
        if client.api_key:
            try:
                # Test the client with a simple call
                test_response = generate_expert_response(client, expert1, topic, conversation_history, is_opening=True)
                if test_response:
                    working_client = client
                    break
            except:
                continue
    
    if not working_client:
        # Fallback mock data
        debate_exchanges = [
            {
                "speaker": expert1,
                "statement": f"You know, I've been thinking a lot about {topic} lately. I think there's so much potential here that we're just beginning to understand.",
                "turn": 1
            },
            {
                "speaker": expert2,
                "statement": f"That's interesting you say that. I actually have some concerns about {topic}. What aspects excite you the most?",
                "turn": 1
            },
            {
                "speaker": expert1,
                "statement": f"Well, mainly the opportunities it creates. But I'm curious - what concerns do you have?",
                "turn": 2
            },
            {
                "speaker": expert2,
                "statement": f"Mainly the ethical implications and long-term effects we might not be considering yet.",
                "turn": 2
            }
        ]
    else:
        # Generate turn-by-turn dialogue
        for turn in range(1, turns + 1):
            # Expert 1's turn
            is_opening = (turn == 1)
            expert1_response = generate_expert_response(working_client, expert1, topic, conversation_history, is_opening)
            if expert1_response:
                debate_exchanges.append({
                    "speaker": expert1,
                    "statement": expert1_response,
                    "turn": turn
                })
                conversation_history.append({"role": "assistant", "content": expert1_response})
            
            # Expert 2's turn
            expert2_response = generate_expert_response(working_client, expert2, topic, conversation_history, is_opening)
            if expert2_response:
                debate_exchanges.append({
                    "speaker": expert2,
                    "statement": expert2_response,
                    "turn": turn
                })
                conversation_history.append({"role": "assistant", "content": expert2_response})

    figure_data = {
        "type": "bar",
        "labels": ["Baseline", "Improved"],
        "values": [random.randint(50, 80), random.randint(60, 95)]
    }

    return jsonify({
        "topic": topic,
        "expert1": expert1,
        "expert2": expert2,
        "exchanges": debate_exchanges,
        "total_turns": turns,
        "figure": figure_data
    })

if __name__ == "__main__":
    app.run(debug=True)
