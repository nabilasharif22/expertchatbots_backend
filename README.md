# Expert Chatbots - Platform

A web application that simulates conversations between historical experts and thought leaders using AI. Users can choose any topic and two experts, and watch them engage in an authentic, intelligent dialogue.

---

##  Architecture Overview

This project consists of two main components:
- **Frontend**: Static HTML/CSS/JavaScript hosted on GitHub Pages
- **Backend**: Flask API deployed on Render (handles OpenAI API calls)

---

##  Frontend

### Description
The frontend is a single-page application that provides an interactive interface for starting and viewing expert debates. It displays two chat panels side-by-side where expert responses appear with smooth animations.

### Files
- `index.html` - Main HTML structure
- `style.css` - Styling and animations
- `script.js` - Client-side logic and API communication

### How It Works

1. **User Input**: User enters a debate topic and two expert names
2. **API Request**: Frontend sends POST request to backend with topic and expert names
3. **Loading State**: Displays "Thinking..." indicators in both chat panels
4. **Response Handling**: Receives conversation exchanges from backend
5. **Message Display**: Animates messages appearing in their respective panels with 2-second delays
6. **Format Compatibility**: Handles both old format (`debate` string) and new format (`exchanges` array)

### Frontend-Backend Communication

**Endpoint Called**: `POST https://expertchatbots-backend.onrender.com/debate`

**When**: Triggered when user submits the debate form

**Request Payload**:
```json
{
  "topic": "AI in education",
  "expert1": "Einstein",
  "expert2": "Curie",
  "turns": 4
}
```

**Expected Response**:
```json
{
  "topic": "AI in education",
  "expert1": "Einstein",
  "expert2": "Curie",
  "exchanges": [
    {
      "speaker": "Einstein",
      "statement": "I've spent considerable time...",
      "turn": 1
    },
    {
      "speaker": "Curie",
      "statement": "That's a compelling perspective...",
      "turn": 1
    }
  ],
  "total_turns": 4,
  "figure": {
    "type": "bar",
    "labels": ["Baseline", "Improved"],
    "values": [66, 86]
  }
}
```

**What Frontend Does With Response**:
- Parses `exchanges` array
- For each exchange, creates a message div
- Assigns message to correct expert panel based on `speaker` field
- Animates messages appearing sequentially with delays
- Handles errors with user-friendly alerts

### How to Run Frontend Locally

```bash
# Navigate to project directory
cd expertchatbots.github.io

# Start a local server (option 1: Python)
python3 -m http.server 8000

# Or (option 2: Node.js)
npx serve

# Open browser
# Visit: http://localhost:8000
```

### Security Note
The frontend **does not** contain any API keys or secrets. All sensitive credentials are stored securely on the backend.

---

##  Backend

### Description
A Flask REST API that generates AI-powered conversations between experts using OpenAI's GPT-4o-mini model. The backend handles all AI requests, prompt engineering, and conversation flow logic.

### Technology Stack
- **Framework**: Flask
- **CORS**: Flask-CORS (allows frontend to make cross-origin requests)
- **AI Provider**: OpenAI API (GPT-4o-mini)
- **Environment**: Python 3.x
- **Dependencies**: `openai`, `flask`, `flask-cors`, `python-dotenv`

### API Endpoints

#### 1. **GET /**
- **Purpose**: Health check endpoint
- **Parameters**: None
- **Returns**: 
  ```json
  {
    "message": "Expert Chatbots Backend Running"
  }
  ```
- **Status Code**: 200

#### 2. **POST /debate**
- **Purpose**: Generate a multi-turn conversation between two experts on a given topic
- **Content-Type**: `application/json`
- **Parameters**:
  | Parameter | Type | Required | Default | Description |
  |-----------|------|----------|---------|-------------|
  | `topic` | string | Yes | - | The subject of the conversation |
  | `expert1` | string | Yes | - | Name of the first expert |
  | `expert2` | string | Yes | - | Name of the second expert |
  | `turns` | integer | No | 4 | Number of back-and-forth exchanges |

- **Request Example**:
  ```json
  {
    "topic": "quantum mechanics",
    "expert1": "Einstein",
    "expert2": "Bohr",
    "turns": 4
  }
  ```

- **Success Response** (200):
  ```json
  {
    "topic": "quantum mechanics",
    "expert1": "Einstein",
    "expert2": "Bohr",
    "exchanges": [
      {
        "speaker": "Einstein",
        "statement": "From my perspective on quantum theory...",
        "turn": 1
      },
      {
        "speaker": "Bohr",
        "statement": "I appreciate your viewpoint, but...",
        "turn": 1
      }
    ],
    "total_turns": 4,
    "figure": {
      "type": "bar",
      "labels": ["Baseline", "Improved"],
      "values": [72, 89]
    }
  }
  ```

- **Error Response** (400):
  ```json
  {
    "error": "Missing topic or expert names"
  }
  ```

### How It Works

1. **Request Validation**: Checks that topic, expert1, and expert2 are provided
2. **API Key Selection**: Tries primary OpenAI API key, falls back to secondary if needed
3. **Conversation Generation**:
   - For each turn, generates expert1's response, then expert2's response
   - Each response is 4-6 sentences and contextually aware of previous messages
   - Uses temperature of 0.9 for creative, authentic responses
   - Max 250 tokens per response
4. **Voice Matching**: AI is prompted to match each expert's authentic speaking style, vocabulary, and intellectual approach
5. **Context Building**: Maintains conversation history so experts respond to each other
6. **Fallback**: If API calls fail, returns mock conversation data

### Environment Setup

#### Required Environment Variables

Create a `.env` file in the backend directory:

```bash
# Primary OpenAI API Key (required)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Secondary OpenAI API Key (optional fallback)
OPENAI_API_KEY_SECOND=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/nabilasharif22/expertchatbots.github.io.git
cd expertchatbots.github.io

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install flask flask-cors openai python-dotenv

# 4. Create .env file
touch .env
# Add your OpenAI API keys to .env (see above)

# 5. Run the backend
python app.py
```

The backend will start on `http://127.0.0.1:5000`

#### Testing the Backend

```bash
# Test health check
curl http://127.0.0.1:5000/

# Test debate endpoint
curl -X POST http://127.0.0.1:5000/debate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "artificial intelligence",
    "expert1": "Turing",
    "expert2": "Lovelace",
    "turns": 2
  }'
```

### Authentication & Security

#### How API Keys Are Handled

 **Secure Practices**:
- API keys are stored in `.env` file on the backend server only
- `.env` file is added to `.gitignore` (never committed to version control)
- Frontend makes requests to backend API, never directly to OpenAI
- Backend acts as a secure proxy between frontend and OpenAI
- CORS is configured to allow requests from authorized origins only

 **What NOT to Do**:
- Never put API keys in frontend JavaScript
- Never commit `.env` file to Git
- Never hardcode API keys in source code

#### Deployment Environment Variables (Render)

When deploying to Render:
1. Go to your Render service dashboard
2. Navigate to "Environment" section
3. Add environment variables:
   - `OPENAI_API_KEY`: Your primary OpenAI API key
   - `OPENAI_API_KEY_SECOND`: (Optional) Your secondary API key

#### API Key Fallback Logic

```python
# Backend tries each API key in order
llm_clients = [
    OpenAI(api_key=os.getenv("OPENAI_API_KEY")),        # Primary
    OpenAI(api_key=os.getenv("OPENAI_API_KEY_SECOND"))  # Fallback
]

# If both fail, returns mock data instead of crashing
```

### Production Deployment

**Current Deployment**: https://expertchatbots-backend.onrender.com

**Deployment Platform**: Render

**Deploy New Version**:
1. Push changes to your backend repository
2. Render automatically detects changes and redeploys
3. Or manually trigger deploy from Render dashboard

### Dependencies

```
flask==3.0.0
flask-cors==4.0.0
openai==1.12.0
python-dotenv==1.0.0
```

---

## Quick Start (Full Stack)

### Frontend Only
```bash
cd expertchatbots.github.io
python3 -m http.server 8000
# Visit http://localhost:8000
```

### Backend + Frontend (Local Development)
```bash
# Terminal 1: Start backend
cd expertchatbots.github.io
python app.py  # Runs on port 5000

# Terminal 2: Start frontend
python3 -m http.server 8000

# Update script.js to use local backend:
# const BACKEND_URL = 'http://127.0.0.1:5000/debate';
```

---

Summary of interactions with ChatGPT (generated by ChatGPT)

---

## 1. Project Overview

The goal of this project was to build a website where two chatbots can converse with each other. The user can define the identity of the chatbots as any expert, with public publications or credentials. The interface is designed to display the chat windows on either side of the screen and evidence graphs in the center.

The project uses a backend API for language models hosted on Render, and a frontend hosted on GitHub Pages. The system is designed to handle multiple API keys to avoid quota limitations.

## 2. Backend Setup

* A Python Flask backend (`app.py`) was created to handle API requests for the chatbot interactions.
* Environment variables are used to store API keys securely.
* Endpoints were implemented to fetch debates and generate chatbot responses.
* Load balancing between multiple API keys was added to manage quota limits.
* Local testing was done to resolve issues such as missing modules and JSON parsing errors.
* Optimizations were added to handle slow responses from the language models.

## 3. Frontend Setup

* The frontend layout was designed with two chat windows on either side and a central area for evidence graphs.
* HTML, CSS, and JavaScript were used to build the interface and handle data fetching.
* Styling was applied to make the interface professional, including readable chat bubbles and responsive layout.
* Error handling was added for fetch failures and slow responses.
* Loading indicators were implemented to improve the user experience.
* Frontend fetch requests were corrected to avoid JSON parsing errors, ensuring proper communication with the backend.

## 4. Deployment

* The backend was deployed to Render, ensuring persistent URLs across commits.
* The frontend was hosted on GitHub Pages.
* Cross-origin and fetch issues were resolved to allow the frontend to communicate with the backend correctly.
* Deployment considerations include consistent endpoint URLs and handling of multiple API keys.

## 5. Enhancements and Features

* Added support for two API keys to manage request limits.
* Debugging tools and logging were used to identify issues with slow chatbot responses.
* Plans for dynamic API switching when quota limits are reached.
* Future enhancements include persistent user chat history and real-time graph updates.

## 6. Common Issues & Fixes

* **Quota errors (429):** Implemented API key switching.
* **Module errors:** Installed missing Python packages.
* **JSON parsing errors:** Corrected backend responses to ensure valid JSON.
* **Fetch failures:** Verified frontend-backend URLs and CORS settings.
* **Slow responses:** Added loading indicators and plan for backend optimization.


Summary of interactions with copilot (generated by copilot)

### What Was Requested
The user wanted to ensure the Flask backend was working properly and needed help diagnosing a "Failed to fetch" error from the frontend. They also requested the debate feature to include structured format with separated expert statements and real turn-by-turn dialogue, rather than a single block of AI-generated text.

### What Was Implemented
1. **Verified and fixed the codebase** - Restored working code after detecting incorrect OpenAI API syntax that was causing deployment failures on Render
2. **Built structured debate system** - Implemented turn-by-turn conversation logic where each expert responds based on previous statements, with clear separation and labeling
3. **Added dual API key failover** - Created resilient system that tries multiple OpenAI API keys sequentially and falls back to mock data if all fail
4. **Created comprehensive validation** - Built test suite (`validate.py`) to verify all endpoints and error handling work correctly
5. **Documented the system** - Updated README to explain the functionality, API endpoints, setup process, and deployment requirements

This section documents the development journey and key improvements made through collaborative iteration.

### Initial Request
**Prompt**: "how do i run this"

**Action Taken**: 
- Analyzed the project structure (HTML, CSS, JS files)
- Started a local HTTP server using Python's built-in server
- Opened the webpage in browser at `http://localhost:8000`
- Explained both double-click and local server options

### Debugging & CORS Issue
**Prompt**: "Error fetching debate: Failed to fetch"

**Problem Identified**: CORS (Cross-Origin Resource Sharing) issue when frontend tried to access backend API from localhost

**Solution Implemented**:
- Modified `script.js` to always use the Render backend URL instead of conditional logic
- Changed from: `const BACKEND_URL = window.location.hostname.includes('github.io') ? RENDER_BACKEND : LOCAL_BACKEND;`
- Changed to: `const BACKEND_URL = RENDER_BACKEND;`

### Frontend-Backend Compatibility
**Prompt**: "imagine app.py is in the backend. make the webpage compatible"

**Problem**: Backend returns `exchanges` array format, but frontend expected `debate` string format

**Solution Implemented**:
- Updated `showMessages()` function to accept structured exchange objects instead of plain strings
- Modified message assignment logic to use `exchange.speaker` and `exchange.statement`
- Improved fetch error handling with proper HTTP status checks
- Added support for both old and new response formats for backward compatibility

### Display Bug Fix
**Prompt**: "the other expert is not shown to respond. also, get rid of the graph feature"

**Solutions Implemented**:
1. **Fixed Expert Display Logic**:
   - Changed from exact string comparison to case-insensitive comparison
   - Added fallback logic to alternate messages if speaker names don't match exactly
   - Used `toLowerCase()` for robust name matching

2. **Removed Graph Feature**:
   - Deleted Chart.js rendering code from `script.js`
   - Removed `#graph-panel` HTML element from `index.html`
   - Removed graph-related CSS styles from `style.css`
   - Cleaned up chart initialization and opacity transitions

### Making Conversations Natural
**Prompt**: "make it seem more like a natural conversation by changing the backend code"

**Improvements Made**:
- Changed prompts from formal "debate" language to casual "conversation"
- Modified system prompts to encourage questions, acknowledgments, and natural responses
- Increased temperature from 0.7 to 0.8 for more human-like variability
- Removed speaker name prefixes from conversation history for cleaner flow
- Updated fallback mock data to demonstrate natural back-and-forth dialogue

### Enhancing Authenticity & Depth
**Prompt**: "increase the delay between each conversation. make sure they are talking long enough so we understand the topic. The experts should incorporate their own findings and considerations about the topic. the tone and voice should match their writing style and how each experts spoke."

**Major Improvements**:
1. **Timing Adjustments**:
   - Increased delay between messages from 800ms to 2000ms (2 seconds)
   - Increased number of turns from 3 to 4 for deeper conversations

2. **Response Length & Quality**:
   - Increased response length from 2-3 sentences to 4-6 sentences
   - Increased max tokens from 150 to 250
   - Raised temperature to 0.9 for more distinctive voices

3. **Expert Voice Authenticity**:
   - Created detailed prompts instructing AI to match each expert's actual speaking/writing style
   - Prompts now require experts to reference their own specific work, experiments, and theories
   - Added instructions to use vocabulary and expressions characteristic of each expert
   - Emphasized staying true to expert's personality, era, and intellectual style

4. **Enhanced Prompts**:
   - Opening prompt: Asks for authentic voice, unique perspective, and 4-6 sentence opening
   - Continuation prompt: Encourages referencing specific work, asking characteristic questions, and using expert's reasoning style
   - Both prompts emphasize being conversational but intellectually substantive

5. **Better Fallback Data**:
   - Updated mock conversations to be longer and more authentic
   - Included references to research, experimental evidence, and theoretical frameworks
   - Demonstrated thoughtful back-and-forth with questions and rebuttals

### Documentation
**Prompt**: "separate the readme into frontend and backend. describe in detail the following: What your backend does... How the frontend communicates... How to set up and run... How authentication or secrets are handled..."

**Documentation Created**:
- Comprehensive README with clear Frontend/Backend separation
- Detailed API endpoint documentation with parameters and examples
- Step-by-step setup instructions for both components
- Security section explaining API key handling and best practices
- Request/response examples for all endpoints
- Quick start guide for different use cases

### Key Technical Decisions

1. **Separation of Concerns**: Frontend handles UI/UX, backend handles AI logic and API keys
2. **Security First**: API keys never exposed to frontend, backend acts as secure proxy
3. **Graceful Degradation**: Fallback mock data if API calls fail
4. **Flexible Format Support**: Frontend handles both old and new response formats
5. **User Experience**: 2-second delays for readability, smooth animations, clear loading states
6. **AI Quality**: High temperature (0.9) + detailed prompts = authentic expert voices



