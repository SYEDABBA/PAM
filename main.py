import os
from scripts.story_generator import generate_episode
from scripts.sherpa_poster import post_to_sherpa

def main():
    print("--- Starting PAM Pipeline ---")
    
    # Episode Input Prompt
    bracket_input = "[सम्राट राय रायज़ादा अपने कमरे में बैठकर नोवेल का आखिरी चैप्टर खत्म करता है और अचानक आसमान लाल हो जाता है तथा सिस्टम रियल वर्ल्ड में लागू होने लगता है]"
    
    # 1. AI Story Generation
    print("Step 1: Generating Episode Content...")
    story_content = generate_episode(bracket_input)
    print("Story Generated Successfully!")
    
    # 2. Extract Title and Content
    lines = story_content.strip().split("\n")
    title = lines[0] if lines else "एपिसोड 1"
    
    # 3. Sherpa Auto-Publishing
    print("Step 2: Publishing to Pocket FM Sherpa...")
    post_to_sherpa(title, story_content)
    print("--- PAM Pipeline Completed Successfully ---")

if __name__ == "__main__":
    main()
