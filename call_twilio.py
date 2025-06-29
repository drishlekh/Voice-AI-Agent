import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def make_call(to_number):
    try:
        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        
        # Use your ngrok URL for the voice webhook
        voice_url = f"{os.getenv('NGROK_URL')}/voice"
        
        print(f"Making call to {to_number}")
        print(f"Voice webhook URL: {voice_url}")
        
        call = client.calls.create(
            to=to_number,
            from_=os.getenv("TWILIO_NUMBER"),
            url=voice_url,  # Twilio will fetch TwiML from this URL
            method="POST"
        )
        print(f"✅ Call initiated successfully!")
        print(f"Call SID: {call.sid}")
        print(f"Call Status: {call.status}")
        
    except Exception as e:
        print(f"❌ Error making call: {e}")

def test_webhook():
    """Test if the webhook URL is accessible"""
    try:
        import requests
        webhook_url = f"{os.getenv('NGROK_URL')}/voice"
        response = requests.get(webhook_url)
        if response.status_code == 200:
            print(f"✅ Webhook URL is accessible: {webhook_url}")
        else:
            print(f"❌ Webhook URL returned status {response.status_code}: {webhook_url}")
    except Exception as e:
        print(f"❌ Cannot reach webhook URL: {e}")

if __name__ == "__main__":
    print("=== Voice AI Agent Call Initiator ===")
    
    # Test webhook first
    print("\n1. Testing webhook URL...")
    test_webhook()
    
    # Make call
    print("\n2. Initiating call...")
    phone = input("Enter the phone number to call (with country code, e.g. +15551234567): ")
    make_call(phone)
    
    print("\n3. Call initiated! Answer your phone and start speaking.")