import os
import google.generativeai as genai
from groq import Groq

SYSTEM_PROMPT = """
तुम एक अनुभवी प्रोफेशनल हिंदी ऑडियो-सीरीज़ लेखक, कहानीकार, स्क्रीनराइटर और स्टोरी एडिटर हो।
तुम्हें एक हिंदी ऑडियो-सीरीज़ लिखनी है जिसका नाम है: "कहानी का जादू" (Kahani Ka Jaadoo)।

━━━━━━━━━━━━━━━━━━
STORY CORE CONCEPT & MC SETUP
━━━━━━━━━━━━━━━━━━
1. CORE CONCEPT: मुख्य पात्र (MC) एक ऐसा लड़का है जो हमेशा एक ही अजीब और रहस्यमयी नोवेल/मैनवा पढ़ता था, जिसे दुनिया में उसके अलावा कोई नहीं पढ़ता था। जब वह उस पूरी कहानी को खत्म कर लेता है, तो उस नोवेल की काल्पनिक दुनिया असल जिंदगी (Real World) में बदल जाती है।
2. MC NAME & BACKGROUND: 'सम्राट राय रायज़ादा' (Samrat Rai Raizada) - रायज़ादा खानदान का वारिस।
3. MC PERSONALITY: सम्राट हर मुश्किल और खतरनाक से खतरनाक सिचुएशन में भी मज़ाक करता रहता है, दुश्मनों को रोस्ट (Roast) करता रहता है और बेहद कूल/सार्केस्टिक रहता है। लेकिन जब वह सीरियस (Serious) होता है, तो सामने वाले की रूह कांप जाती है।
4. DIALOGUE & LANGUAGE: पूरी बातचीत आधुनिक, सरल और स्वाभाविक हिंदी में होगी। सम्राट का अंदाज़ स्वैगी, कूल और मज़ाकिया होगा।

━━━━━━━━━━━━━━━━━━
RULES
━━━━━━━━━━━━━━━━━━
1. हर एपिसोड कम से कम 2000 से 2500 शब्दों का होना अनिवार्य है।
2. बेकार का Filler मत डालो। हर सीन कहानी को आगे बढ़ाए।
3. AI Voice (TTS) Optimization: वाक्य ज्यादा लंबे न हों, सही विराम चिन्ह हों।
4. हर एपिसोड के अंत में एक ज़बरदस्त Cliffhanger होना चाहिए।

━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT
━━━━━━━━━━━━━━━━━━
एपिसोड [नंबर]: [आकर्षक हिंदी शीर्षक]

(इसके बाद सीधे 2000+ शब्दों की कहानी शुरू करो।)
"""

def try_groq(prompt: str) -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing in environment variables.")
        
    client = Groq(api_key=api_key)
    groq_models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768"
    ]
    
    for model_name in groq_models:
        try:
            print(f"Trying Groq Model: {model_name}...")
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model_name,
                temperature=0.7,
                max_tokens=4096
            )
            res = completion.choices[0].message.content
            if res and len(res.strip()) > 100:
                print(f"✅ Success with Groq model: {model_name}")
                return res
        except Exception as e:
            print(f"❌ Groq {model_name} failed: {e}")
            continue
            
    raise RuntimeError("All Groq models failed.")

def try_gemini(prompt: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing in environment variables.")
        
    genai.configure(api_key=api_key)
    
    # Static fallbacks without prefix issues
    fallback_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"]
    active_models = []
    
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                clean_name = m.name.replace("models/", "")
                # Skip TTS/Audio specialized models that break text generation
                if "tts" not in clean_name and "audio" not in clean_name:
                    active_models.append(clean_name)
    except Exception as e:
        print(f"Warning fetching models: {e}")
        
    # Merge dynamically fetched models with fallback list
    candidate_models = list(dict.fromkeys(active_models + fallback_models))
    print(f"Candidate Gemini Models to try: {candidate_models}")

    for model_name in candidate_models:
        try:
            print(f"Trying Gemini Model: {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            if response and response.text and len(response.text.strip()) > 100:
                print(f"✅ Success with Gemini model: {model_name}")
                return response.text
        except Exception as e:
            print(f"❌ Gemini {model_name} failed: {e}")
            continue
            
    raise RuntimeError("All Gemini models failed.")

def generate_episode(bracket_input: str) -> str:
    full_prompt = f"{SYSTEM_PROMPT}\n\n[USER INPUT]:\n{bracket_input}"
    
    # 1. Groq Try karo
    try:
        return try_groq(full_prompt)
    except Exception as e:
        print(f"⚠️ Groq failed: {e}. Switching to Gemini...")

    # 2. Gemini Try karo
    try:
        return try_gemini(full_prompt)
    except Exception as e:
        print(f"⚠️ Gemini failed: {e}")

    raise RuntimeError("🚨 ALL AI Models failed! Check your API keys in GitHub Secrets.")

if __name__ == "__main__":
    test_input = "[सम्राट राय रायज़ादा अपने कमरे में बैठकर नोवेल का आखिरी चैप्टर खत्म करता है और अचानक आसमान लाल हो जाता है तथा सिस्टम रियल वर्ल्ड में लागू होने लगता है]"
    print(generate_episode(test_input))
