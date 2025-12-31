# 🌾 AgriSathi (Krishi Sakhi)
### AI-Powered Personal Farming Assistant for Kerala & South India

AgriSathi is a complete, production-ready AI Farming Assistant designed to provide actionable, region-specific, and multilingual advice to farmers.

---

## 🌟 Key Features
- **Multilingual AI Assistant**: Smart chat support in English, Malayalam, and Tamil.
- **Voice Enabled**: Full Speech-to-Text (STT) and Text-to-Speech (TTS) integration.
- **Smart Dashboard**: Real-time weather, personalized alerts, and government news.
- **Crop Advisor**: ML-powered crop recommendation and Leaf Disease diagnosis.
- **Govt Schemes & News**: Curated Kerala-specific agricultural programs.
- **Farm Records**: Secure storage for AI advice and important documents.
- **Offline Fallback**: Intelligent rule-based engine when API limits are reached.

## 🛠 Tech Stack
- **Backend**: FastAPI (Python 3.10+), SQLite (SQLAlchemy), OpenAI (GPT-4o & Whisper), gTTS.
- **Frontend**: Vanilla JS, HTML5, Tailwind CSS (Mobile-first design).
- **Environment**: Configured via `.env` for production keys.

---

## 🚀 Setup Instructions

### 1. Backend Setup
1. **Navigate to backend**:
   ```ps
   cd backend
   ```
2. **Install dependencies**:
   ```ps
   pip install -r requirements.txt
   ```
3. **Set Environment Variables**:
   In `backend/.env`, ensure you have:
   - `OPENAI_API_KEY`: For AI Chat, Voice, and Transcriptions.
   - `OPENWEATHER_API_KEY`: For real-time weather alerts.
   - `NEWS_API_KEY`: For agricultural news updates.

4. **Run Server**:
   ```ps
   uvicorn app.main:app --reload --port 8001
   ```

### 2. Frontend Setup
1. **Open the App**:
   Simply open `frontend/index.html` in any modern browser.
2. **First Use**:
   - Register a new account.
   - Select your language (English/Malayalam/Tamil).
   - Click the Microphone icon in the AI Assistant to start a voice conversation.

---

## 💡 Usage Rule
**AgriSathi exists to help farmers.** 
- If a question is about crops, pests, soil, or any farming topic, it will provide a structured answer:
  1. **Short Answer** (Direct)
  2. **Detailed Guidance** (Practical steps)
  3. **Farmer Tip** (Pro-advice)

---

## 📂 Project Structure
```text
project/
├── backend/
│   ├── app/
│   │   ├── api/routes/    # Auth, Assistant, Weather, Schemes, etc.
│   │   ├── services/      # AI, TTS, Assistant Logic
│   │   ├── models/        # Database Schemas
│   │   └── main.py        # FastAPI Entry point
│   ├── .env               # Secrets
│   └── agrisathi.db       # Database
└── frontend/
    ├── index.html         # Unified Mobile-first UI
```
