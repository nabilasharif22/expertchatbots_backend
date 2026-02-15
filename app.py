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
        system_prompt = f"""You are {expert_name}. Speak in YOUR authentic voice and style - use the vocabulary, tone, and manner of expression that {expert_name} was known for. 
        
You're having a conversation about {topic}. Give an opening statement that:
- Reflects YOUR unique perspective and expertise (4-6 sentences)
- Incorporates specific findings, theories, or considerations that {expert_name} would actually reference
- Uses language and phrasing characteristic of how {expert_name} communicated
- Sounds natural and conversational, not rehearsed

Be authentic to {expert_name}'s worldview, era, and intellectual style."""
    else:
        system_prompt = f"""You are {expert_name}. Continue speaking in YOUR authentic voice and style.
        
Respond to what was just said (4-6 sentences):
- Reference YOUR specific work, experiments, or theories when relevant
- Ask thoughtful questions that {expert_name} would actually ask
- Challenge or build on ideas using {expert_name}'s characteristic reasoning style
- Use vocabulary and expressions that match how {expert_name} actually spoke/wrote
- Be conversational but intellectually substantive

Stay true to {expert_name}'s personality, expertise, and historical context."""
    
    messages = [{"role": "system", "content": system_prompt}] + conversation_history
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.9,
            max_tokens=250
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
    turns = data.get("turns", 4)  # Number of back-and-forth exchanges

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
                "statement": f"I've spent considerable time examining {topic}, and I must say, the fundamental principles at work here are quite fascinating. Based on my research and observations, I believe we're dealing with forces that could fundamentally reshape how we understand this domain. The theoretical framework I've been developing suggests there are profound implications we haven't fully explored yet. What's your initial take on this?",
                "turn": 1
            },
            {
                "speaker": expert2,
                "statement": f"That's a compelling perspective, though I find myself approaching {topic} from a somewhat different angle. In my own work, I've encountered certain challenges that make me question some of the prevailing assumptions. The experimental evidence I've gathered points to complexities that aren't immediately obvious. I'm particularly concerned about the practical applications and whether we've adequately considered the long-term consequences. Have you encountered similar concerns in your research?",
                "turn": 1
            },
            {
                "speaker": expert1,
                "statement": f"Your concerns are valid, and I appreciate the empirical rigor you bring to this discussion. However, my findings suggest that many of these challenges can be addressed through systematic analysis and careful methodology. I've observed patterns that indicate the benefits could far outweigh the risks, provided we approach this with the proper intellectual framework. The key, I believe, lies in understanding the underlying mechanisms at a deeper level.",
                "turn": 2
            },
            {
                "speaker": expert2,
                "statement": f"I respect your theoretical approach, but I must emphasize what I've learned through direct experimentation and observation. Theory is essential, certainly, but we must ground our conclusions in reproducible results and practical realities. In my laboratory work on related phenomena, I've discovered that the gap between theoretical predictions and actual outcomes can be substantial. We need to remain cautious and methodical rather than rushing forward based on promising hypotheses alone.",
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
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
