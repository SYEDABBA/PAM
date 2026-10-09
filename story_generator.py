import os
from google import genai
from groq import Groq

SYSTEM_PROMPT = """
तुम एक अनुभवी प्रोफेशनल हिंदी ऑडियो-सीरीज़ लेखक हो।
तुम्हें ऑडियो-सीरीज़ "कहानी का जादू" (Kahani Ka Jaadoo) के लिए रोज़ाना 2 एपिसोड लिखने हैं।

Pocket FM Guidelines Strict Rules:
1. पूरी कहानी केवल 100% शुद्ध देवनागरी हिंदी लिपि में होनी चाहिए।
2. एक भी अंग्रेजी अक्षर (A-Z) या रोमन शब्द का प्रयोग बिल्कुल न करें।
3. किसी भी प्रकार के साउंड इफेक्ट्स, ब्रैकेट (), [], सीन डिस्क्रिप्शन या नैरेटर टैग्स मत लिखो। सीधे कहानी और संवाद लिखो।
4. कहानी का प्रवाह ऐसा होना चाहिए जिसे सीधे ऑडियो में पढ़ा जा सके।
5. हर एपिसोड कम से कम 2000 शब्दों का होना चाहिए।
6. मुख्य पात्र 'सम्राट राय रायज़ादा' का सार्केस्टिक और रोस्टिंग अंदाज़ बना रहना चाहिए।
7. एपिसोड के अंत में एक ज़बरदस्त सस्पेंस/क्लिफहैंगर होना अनिवार्य है।
"""

def generate_episode(prompt_text: str) -> str:
    groq_api_key = os.environ.get("GROQ_API_KEY")
    gemini_api_key = os.environ.get("GEMINI_API_KEY")

    full_prompt = f"{SYSTEM_PROMPT}\n\n[एपिसोड निर्देश]:\n{prompt_text}"

    # Try Groq First
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": full_prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=4096
            )
            res = completion.choices[0].message.content
            if res and len(res.strip()) > 100:
                return res
        except Exception as e:
            print(f"Groq failed: {e}")

    # Fallback to New Gemini SDK (google-genai)
    if gemini_api_key:
        try:
            client = genai.Client(api_key=gemini_api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt,
            )
            if response and response.text:
                return response.text
        except Exception as e:
            print(f"Gemini failed: {e}")

    raise RuntimeError("All AI models failed to generate episode.")
