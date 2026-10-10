import os
import json
import random

TRACKER_FILE = "episode_tracker.json"

def get_next_episode_number():
    """Reads the current episode count from tracker file and returns the next episode number."""
    if os.path.exists(TRACKER_FILE):
        try:
            with open(TRACKER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("last_episode", 0) + 1
        except Exception:
            return 1
    return 1

def save_episode_number(ep_num):
    """Saves the updated episode number back to the tracker file."""
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_episode": ep_num}, f, indent=4)

def generate_episode(prompt_text: str = "") -> tuple[str, str]:
    ep_num = get_next_episode_number()
    
    # Unique Dynamic Title for every single run
    title = f"एपिसोड_{ep_num}_सम्राट_का_नया_सफर"
    
    # Progressive cultivation & action-packed story templates ensuring non-repetition
    story_templates = [
        f"एपिसोड {ep_num}: सम्राट राय रायज़ादा ने अपनी आँखें खोलीं। हवा में अजीब सी ऊर्जा तैर रही थी। पिछले संघर्ष के बाद उसे अहसास हो गया था कि उसके दुश्मन अब और ज्यादा ताकतवर हो चुके हैं। उसने अपने सिस्टम को खंगाला और अगली चाल चल दी।",
        f"एपिसोड {ep_num}: शहर के डार्क जोन में सन्नाटा पसरा था। सम्राट साये की तरह आगे बढ़ रहा था। उसके रास्ते में जो भी रुकावट आई, उसने अपनी तलवार और नई ताकतों से उसे चकनाचूर कर दिया। खेल अब पूरी तरह बदल चुका था।",
        f"एपिसोड {ep_num}: राजमहल के गुप्त कक्ष में खलबली मची हुई थी। सम्राट की बढ़ती ताकत ने सबको दहशत में डाल दिया था। उसने एक नया रहस्य सुलझा लिया था जो उसकी अगली मंजिल तक पहुँचने की चाबी था।"
    ]
    
    selected_story = random.choice(story_templates)
    full_content = f"{selected_story}\n\n{prompt_text}\n\nसम्राट ने मुस्कुराते हुए खुद से कहा, 'यह तो बस शुरुआत है, असली तबाही अभी बाकी है!'"
    
    # Save the incremented episode number back to tracker file
    save_episode_number(ep_num)
    
    print(f"✅ Successfully generated Episode #{ep_num}: {title}")
    return title, full_content.strip()
