# llm_utils.py
import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def ask_groq(prompt, max_retries=3):
    """
    Groq API call with retries.
    Fast and reliable cloud-based LLM.
    """
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise Exception("GROQ_API_KEY not found in environment variables. Please add it to .env file.")
    
    client = Groq(api_key=groq_api_key)
    
    for attempt in range(max_retries):
        try:
            print(f"  → Calling Groq API (attempt {attempt+1})...")
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",  # Fastest model on Groq
                temperature=0.5,
                max_tokens=2000,
                timeout=30,
            )
            response_text = chat_completion.choices[0].message.content
            print(f"  ✅ Groq response received ({len(response_text)} chars)")
            return response_text
        except Exception as e:
            print(f"  ⚠️ Groq API attempt {attempt+1} failed: {e}")
            time.sleep(2)
    
    raise Exception("Groq API failed after multiple retries.")