import os
import json
from openai import OpenAI
from groq import Groq
import google.generativeai as genai

TRACKER_FILE = "episode_tracker.json"

def get_next_episode_number():
    if os.path.exists(TRACKER_FILE):
        try:
            with open(TRACKER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("last_episode", 0) + 1
        except Exception:
            return 1
    return 1

def save_episode_number(ep_num):
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_episode": ep_num}, f, indent=4)

def generate_episode(prompt_text: str = "") -> tuple[str, str]:
    ep_num = get_next_episode_number()
    title = f"एपिसोड_{ep_num}_सम्राट_का_नया_सफर"
    
    system_instruction = (
        "You are an elite Hindi audio-series scriptwriter for Pocket FM shows. "
        "You write highly engaging, unique, non-repeating, and detailed 2000+ word episodes "
        "written purely in Devanagari Hindi script. You strictly avoid repeating paragraphs or sentences."
    )
    
    full_prompt = (
        f"आप 'कहानी का जादू' शो के लिए एपिसोड {ep_num} लिखिए। "
        f"मुख्य पात्र 'सम्राट राय रायज़ादा' है। यह कहानी एक्शन, कल्टीवेशन, मिस्ट्री और सस्पेंस से भरपूर होनी चाहिए। "
        f"कृपया बिना किसी लाइन या पैराग्राफ को दोहराए, कम से कम 2000 शब्दों (2000+ words) की एक विस्तृत, रोमांचक और शुद्ध देवनागरी हिंदी स्क्रिप्ट लिखिए। "
        f"इसमें दृश्यों का वर्णन, संवाद (Dialogues) और सम्राट की आंतरिक सोच शामिल करें। {prompt_text}"
    )

    story_content = ""

    # 1. Primary Engine: OpenAI API
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if openai_api_key:
        try:
            print("Generating 2000+ word script using OpenAI API...")
            client = OpenAI(api_key=openai_api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.8,
                max_tokens=4000
            )
            story_content = response.choices[0].message.content
        except Exception as e:
            print(f"[Notice] OpenAI API error: {e}")

    # 2. Secondary Fallback: Groq API
    if not story_content or len(story_content) < 500:
        groq_api_key = os.environ.get("GROQ_API_KEY")
        if groq_api_key:
            try:
                print("Falling back to Groq API...")
                client = Groq(api_key=groq_api_key)
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": full_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4096
                )
                story_content = completion.choices[0].message.content
            except Exception as e:
                print(f"[Notice] Groq API error: {e}")

    # 3. Tertiary Fallback: Gemini API
    if not story_content or len(story_content) < 500:
        gemini_api_key = os.environ.get("GEMINI_API_KEY")
        if gemini_api_key:
            try:
                print("Falling back to Gemini API...")
                genai.configure(api_key=gemini_api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(full_prompt)
                story_content = response.text
            except Exception as e:
                print(f"[Notice] Gemini API error: {e}")

    full_output = f"=== {title} ===\n\n{story_content.strip()}"
    save_episode_number(ep_num)
    
    print(f"✅ Generated Episode #{ep_num} uniquely ({len(full_output)} characters)")
    return title, full_output
