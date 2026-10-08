import os
import google.generativeai as genai

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

def generate_episode(bracket_input: str) -> str:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    # Fixed model name here
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    full_prompt = f"{SYSTEM_PROMPT}\n\n[USER INPUT]:\n{bracket_input}"
    response = model.generate_content(full_prompt)
    return response.text

if __name__ == "__main__":
    test_input = "[सम्राट राय रायज़ादा अपने कमरे में बैठकर नोवेल का आखिरी चैप्टर खत्म करता है और अचानक आसमान लाल हो जाता है तथा सिस्टम रियल वर्ल्ड में लागू होने लगता है]"
    print(generate_episode(test_input))
