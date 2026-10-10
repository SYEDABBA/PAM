import os
import sys
from google import genai
from google.genai import types
from groq import Groq

SYSTEM_PROMPT = """You are a professional Hindi story writer for Pocket FM.
Write an engaging audio story episode in pure Devanagari Hindi.
Rules:
1. Write 100% pure Devanagari Hindi text only.
2. Absolutely NO English words, NO Roman letters (A-Z).
3. Do NOT include brackets (), [], sound effects, or narrator tags.
4. Keep the main character 'Samrat' sarcastic and engaging.
5. End with a huge cliffhanger.
"""

def generate_episode(prompt_text: str) -> str:
    groq_api_key = os.environ.get("GROQ_API_KEY")
    gemini_api_key = os.environ.get("GEMINI_API_KEY")

    # Force check what's going on
    print(f"DEBUG_CHECK -> GROQ_API_KEY Length: {len(groq_api_key) if groq_api_key else 0}")
    print(f"DEBUG_CHECK -> GEMINI_API_KEY Length: {len(gemini_api_key) if gemini_api_key else 0}")

    if not groq_api_key and not gemini_api_key:
        raise RuntimeError("CRITICAL: Both GROQ_API_KEY and GEMINI_API_KEY are missing from environment!")

    full_prompt = f"{SYSTEM_PROMPT}\n\n[Topic / Instructions]:\n{prompt_text}"

    # Try Gemini First
    if gemini_api_key and len(gemini_api_key.strip()) > 5:
        for model_name in ["gemini-2.5-flash", "gemini-1.5-flash"]:
            try:
                client = genai.Client(api_key=gemini_api_key)
                response = client.models.generate_content(
                    model=model_name,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.7,
                        max_output_tokens=4096
                    )
                )
                if response and response.text and len(response.text.strip()) > 50:
                    print(f"Successfully generated episode via Gemini ({model_name})!")
                    return response.text.strip()
            except Exception as e:
                print(f"GEMINI_ERROR_{model_name}: {repr(e)}", file=sys.stderr)

    # Fallback to Groq
    if groq_api_key and len(groq_api_key.strip()) > 5:
        try:
            client = Groq(api_key=groq_api_key)
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": full_prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=4096
            )
            res = completion.choices[0].message.content
            if res and len(res.strip()) > 50:
                print("Successfully generated episode via Groq!")
                return res.strip()
        except Exception as e:
            print(f"GROQ_ERROR: {repr(e)}", file=sys.stderr)

    raise RuntimeError("All AI models execution failed or keys were invalid.")
