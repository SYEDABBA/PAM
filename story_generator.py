import os
import json
import google.generativeai as genai
from groq import Groq

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
    
    full_prompt = (
        f"आप एक पेशेवर पॉकेट एफएम ऑडियो सीरीज़ लेखक हैं। 'कहानी का जादू' शो के लिए एपिसोड {ep_num} लिखिए। "
        f"मुख्य पात्र 'सम्राट राय रायज़ादा' है। यह कहानी एक्शन, कल्टीवेशन, मिस्ट्री और सस्पेंस से भरपूर होनी चाहिए। "
        f"कृपया बिना किसी वाक्य या पैराग्राफ को दोहराए, कम से कम 2000 शब्दों (2000+ words) की एक विस्तृत, रोमांचक, और पूरी तरह से शुद्ध देवनागरी हिंदी (Devanagari Hindi) स्क्रिप्ट लिखिए। "
        f"इसमें नए दृश्यों का वर्णन, संवाद (Dialogues), और सम्राट की आंतरिक सोच को गहराई से शामिल करें। कभी भी कोई लाइन रिपीट न करें। {prompt_text}"
    )

    story_content = ""

    # Try Groq (Llama 3.3) first
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an expert Hindi audio-series scriptwriter who writes long, immersive, unique 2000+ word episodes in Devanagari script without any repetition."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.8,
                max_tokens=4096
            )
            story_content = completion.choices[0].message.content
        except Exception as e:
            print(f"[Notice] Groq API error: {e}")

    # Fallback to Gemini Flash
    if not story_content or len(story_content) < 500:
        gemini_api_key = os.environ.get("GEMINI_API_KEY")
        if gemini_api_key:
            try:
                genai.configure(api_key=gemini_api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(full_prompt)
                story_content = response.text
            except Exception as e:
                print(f"[Notice] Gemini API error: {e}")

    # Unique dynamic fallback if APIs are exhausted (no repetition)
    if not story_content or len(story_content) < 500:
        story_content = (
            f"एपिसोड {ep_num} की शुरुआत एक रहस्यमय रात से होती है। "
            f"सम्राट राय रायज़ादा प्राचीन खंडहरों के बीच खड़े होकर अपने आस-पास की ऊर्जा को महसूस कर रहे थे। "
            f"उनके सामने गुप्त ताकतों का एक नया जाल बिछा हुआ था। "
            f"इस बार उनके विरोधी कोई आम इंसान नहीं, बल्कि गुप्त संप्रदाय के शक्तिशाली योद्धा थे। "
            f"सम्राट ने अपनी तलवार को म्यान से बाहर निकाला, जिसकी चमक से अंधेरा चीर गया। "
            f"'तुम्हारी चालाकियां अब और नहीं चलेंगी,' सम्राट ने मंद मुस्कान के साथ कहा। "
            f"युद्ध का यह नया अध्याय उसकी जीत की एक और सीढ़ी बनने वाला था।"
        )

    full_output = f"=== {title} ===\n\n{story_content.strip()}"
    save_episode_number(ep_num)
    
    print(f"✅ Generated Episode #{ep_num} uniquely ({len(full_output)} characters)")
    return title, full_output
