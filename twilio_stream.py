import os
import requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Helper: Send text to Groq LLM and get response
def ask_groq(prompt):
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant. Keep responses short and conversational for phone calls, under 50 words."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 100,
            "temperature": 0.7
        }
        resp = requests.post(url, headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq API error: {e}")
        return "I'm sorry, I'm having trouble processing your request right now."

@app.get("/")
def read_root():
    return {"message": "Voice AI Agent is running!"}

@app.api_route("/voice", methods=["GET", "POST"])
async def voice(request: Request):
    print("📞 Twilio voice call received!")
    
    # Initial greeting when call starts
    message = "Hello! I am your AI assistant. How can I help you today?"
    
    print(f"📞 AI says: {message}")
    
    # Return TwiML to make Twilio speak and listen
    response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">{message}</Say>
    <Gather input="speech" action="/process-speech" method="POST" speechTimeout="5" timeout="10">
        <Say>Please speak now.</Say>
    </Gather>
    <Say>I didn't hear anything. Goodbye!</Say>
</Response>"""
    
    return Response(content=response, media_type="application/xml")

@app.api_route("/process-speech", methods=["POST"])
async def process_speech(request: Request):
    form = await request.form()
    user_speech = form.get("SpeechResult", "")
    confidence = form.get("Confidence", "0")
    
    print(f"📞 User said: '{user_speech}' (confidence: {confidence})")
    
    if user_speech and user_speech.strip():
        # Send to Groq LLM
        ai_response = ask_groq(user_speech)
        print(f"📞 AI responds: {ai_response}")
        
        # Continue conversation
        response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">{ai_response}</Say>
    <Gather input="speech" action="/process-speech" method="POST" speechTimeout="5" timeout="10">
        <Say>Is there anything else I can help you with?</Say>
    </Gather>
    <Say>Thank you for calling. Goodbye!</Say>
</Response>"""
    else:
        # No speech detected
        response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>I didn't hear anything clearly. Let me try again.</Say>
    <Gather input="speech" action="/process-speech" method="POST" speechTimeout="5" timeout="10">
        <Say>Please speak clearly.</Say>
    </Gather>
    <Say>Thank you for calling. Goodbye!</Say>
</Response>"""
    
    return Response(content=response, media_type="application/xml")

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Voice AI Agent is running"}

# Graceful shutdown
@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down Voice AI Agent...")