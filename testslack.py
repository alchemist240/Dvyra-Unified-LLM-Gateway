import requests
import os
from dotenv import load_dotenv

# 1. Load variables from .env
load_dotenv()

# 2. Get the URL securely
FRESH_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

if not FRESH_WEBHOOK_URL:
    print("❌ ERROR: DISCORD_WEBHOOK_URL not found in .env file.")
    exit()

# 3. Format it correctly (Discord needs /slack for this format)
if not FRESH_WEBHOOK_URL.endswith("/slack"):
    TARGET_URL = FRESH_WEBHOOK_URL + "/slack"
else:
    TARGET_URL = FRESH_WEBHOOK_URL

print(f"🚀 Testing Webhook...")

# 4. Send the POST request
try:
    response = requests.post(
        TARGET_URL, 
        json={"text": "🔔 Hello! If you see this, the connection is PERFECT."}
    )
    
    if response.status_code == 200:
        print("✅ SUCCESS! Check your Discord channel.")
    else:
        print(f"❌ ERROR: {response.text}")

except Exception as e:
    print(f"❌ CRITICAL FAIL: {e}")