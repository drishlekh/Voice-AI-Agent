# Voice-AI-Agent
A real-time conversational AI agent using LiveKit, Groq, ElevenLabs, Deepgram and Silero.


# Voice-AI-Agent

A real-time conversational AI agent built with LiveKit, leveraging powerful AI services for seamless voice interactions. This project demonstrates an agent capable of understanding spoken language, generating intelligent responses, and speaking them back in real-time. It also includes comprehensive metrics logging for performance analysis.

## Features

* **Real-time Voice Interaction:** Connects to LiveKit for bidirectional audio streaming.
* **Speech-to-Text (STT):** Utilizes Deepgram for accurate and fast transcription.
* **Large Language Model (LLM):** Powered by Groq for quick and conversational AI responses.
* **Text-to-Speech (TTS):** Leverages ElevenLabs for natural-sounding voice synthesis.
* **Voice Activity Detection (VAD):** Employs Silero for efficient end-of-utterance detection.
* **Comprehensive Metrics Logging:** Tracks and saves performance metrics for STT, LLM, TTS, and End-of-Utterance (EOU) to an `all_metrics.csv` file for detailed analysis.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/drishlekh/Voice-AI-Agent.git](https://github.com/drishlekh/Voice-AI-Agent.git)
    cd Voice-AI-Agent
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Environment Variables:** Create a `.env` file in the root directory and add your API keys:
    ```
    LIVEKIT_API_KEY="your_livekit_api_key"
    LIVEKIT_API_SECRET="your_livekit_api_secret"
    LIVEKIT_URL="your_livekit_instance_url" # e.g., ws://localhost:7880 or your cloud LiveKit URL
    DEEPGRAM_API_KEY="your_deepgram_api_key"
    GROQ_API_KEY="your_groq_api_key"
    ELEVENLABS_API_KEY="your_elevenlabs_api_key"
    ```

## Usage

### Running Locally

To run the voice agent, ensure you have a LiveKit server running (https://agents-playground.livekit.io/) and your `.env` variables are correctly set.

```bash
python main.py
