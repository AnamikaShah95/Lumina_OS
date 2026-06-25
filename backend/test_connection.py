import sys
import os
from google import genai

# Aapki direct credential key
DIRECT_KEY = "AQ.Ab8RN6JWxNpz4miOjEFDtQRXzFk-A7ynbPHh8IyIG0aiQUYuzg"

def validate_api_connection():
    print("🔄 Checking API credentials boundary using new Google GenAI SDK...")
    
    try:
        # Naye SDK ke mutabik Client initialize karein
        client = genai.Client(api_key=DIRECT_KEY)
        
        print("🛰️ Pinging Gemini API model interface (gemini-2.5-flash)...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents="Ping! System status query. Respond with 'System Active'."
        )
        
        print(f"📡 API Response: {response.text.strip()}")
        print("✅ Success: Connection Validation Passed!")
        return True
        
    except Exception as e:
        print(f"❌ Connection Failed: {str(e)}")
        return False

if __name__ == "__main__":
    validate_api_connection()