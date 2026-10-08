import os
import re
from story_generator import generate_episode
from sherpa_poster import post_to_sherpa

def save_story_locally(title: str, content: str):
    # 'my work' folder create karo agar nahi hai
    folder_name = "my work"
    os.makedirs(folder_name, exist_ok=True)
    
    # File name safe banao (special characters hata kar)
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
    if not safe_title:
        safe_title = "episode_output"
        
    file_path = os.path.join(folder_name, f"{safe_title}.txt")
    
    # Text file me save karo
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"TITLE: {title}\n")
        f.write("="*40 + "\n\n")
        f.write(content)
        
    print(f"📁 Story successfully saved locally at: {file_path}")

def main():
    bracket_input = "[सम्राट राय रायज़ादा अपने कमरे में बैठकर नोवेल का आखिरी चैप्टर खत्म करता है और अचानक आसमान लाल हो जाता है तथा सिस्टम रियल वर्ल्ड में लागू होने लगता है]"
    
    print("Step 1: Generating Story Content...")
    story_content = generate_episode(bracket_input)
    
    # Story title extract karo ya default set karo
    title = "एपिसोड 1: सिस्टम का आगमन"
    lines = story_content.strip().split('\n')
    if lines and "एपिसोड" in lines[0]:
        title = lines[0].replace('#', '').strip()
        
    # 1. Local 'my work' folder me save karo
    save_story_locally(title, story_content)
    
    # 2. Sherpa Poster call karo
    print("Step 2: Publishing to Pocket FM Sherpa...")
    post_to_sherpa(title, story_content)

if __name__ == "__main__":
    main()
