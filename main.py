from story_generator import generate_episode
from sherpa_poster import post_to_sherpa

def main():
    print("==========================================")
    print("🚀 Starting YUGRAAL 10-Min Episode Pipeline")
    print("==========================================")
    
    print("\nStep 1: Generating Unique 2000+ Word Episode...")
    title, story_content = generate_episode("कहानी का जादू - नया रोमांचक पड़ाव")

    print(f"\nStep 2: Processing and Storing Episode: {title}")
    post_to_sherpa(title, story_content)
    
    print("\n✨ Pipeline execution completed successfully!")

if __name__ == "__main__":
    main()
