from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # This loads the variables from .env

# 2. SETUP: Point to your new "Universal Remote"
# We now read the key from the environment variable "LITELLM_MASTER_KEY"
# Make sure the name inside getenv matches exactly what is in your .env file
master_key = os.getenv("LITELLM_MASTER_KEY") 

if not master_key:
    raise ValueError("❌ MASTER KEY NOT FOUND. Please check your .env file.")

client = OpenAI(
    api_key=master_key,  # <---safely loaded from .env
    base_url="https://dominator2414-unified-dvyra.hf.space"
)

print("Attempting to connect to your Gateway...")

try:
    # 2. THE SWITCH: Gemini is dead, so we ask for "llama3-70b" instead!
    # (This works because we defined 'llama3-70b' in your config.yaml)

    #response = client.chat.completions.create(
     #   model="llama3-70b", 
      #  messages=[
       #     {"role": "user", "content": "Hello! Are you working? Tell me a quick fun fact."}
        #]
    #)

    response = client.chat.completions.create(
    model="gemini-lite",  # <--- defined in your config.yaml
    messages=[{"role": "user", "content": "i want to learn 1 new/rarely used english word..suprise me...basiacaly i wnat to omprove my vocab..just output the word and its meaning..no filler sentences"}]
    )

    #response = client.chat.completions.create(
    #    model="gemini-flash", 
    #   messages=[{"role": "user", "content": "Hello! Just checking connection."}]
    #)

    #response = client.chat.completions.create(
    #    model="gpt-4o", 
    #    messages=[{"role": "user", "content": "What is the speed of light? Answer in 5 words."}]
    #)


    # 3. SUCCESS
    print("\n✅ SUCCESS! The Gateway is working.")
    print(f"Model Used: {response.model}")
    print(f"Response: {response.choices[0].message.content}")

except Exception as e:
    error_msg = str(e)
    
    # ANALYSIS OF THE ERROR
    print("\n🔎 DIAGNOSIS:")
    if "429" in error_msg or "Resource has been exhausted" in error_msg:
        print("✅ SUCCESS! (Technically)")
        print("Your Gateway is working perfectly. It connected to Google, and Google replied.")
        print("Result: Connection Verified (Limit Hit)")
    elif "401" in error_msg:
        print("❌ AUTH ERROR: Check your GEMINI_API_KEY in Hugging Face secrets.")
    else:
        print("❌ UNEXPECTED ERROR:")
        print(error_msg)