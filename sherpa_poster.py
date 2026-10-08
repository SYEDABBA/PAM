import os
import json
from playwright.sync_api import sync_playwright

def post_to_sherpa(episode_title: str, episode_content: str):
    # Secret se cookies/storage state read karna
    storage_state_env = os.environ.get("STORAGE_STATE_JSON")
    
    # State data ko temporary load karna
    if storage_state_env:
        try:
            state_data = json.loads(storage_state_env)
            # Standard cookies format ko Playwright format me adapt karna (if array)
            if isinstance(state_data, list):
                state_data = {"cookies": state_data, "origins": []}
            with open("state.json", "w") as f:
                json.dump(state_data, f)
            storage_path = "state.json"
        except Exception as e:
            print(f"Error parsing STORAGE_STATE_JSON: {e}")
            storage_path = None
    else:
        storage_path = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        if storage_path and os.path.exists(storage_path):
            context = browser.new_context(storage_state=storage_path)
        else:
            context = browser.new_context()

        page = context.new_page()

        print("Navigating to Sherpa Dashboard...")
        page.goto("https://sherpa.pocketfm.com/dashboard", timeout=60000)
        
        # Dashboard load verification
        print("Page Title:", page.title())
        
        # Clean up temp file
        if os.path.exists("state.json"):
            os.remove("state.json")

        browser.close()

if __name__ == "__main__":
    post_to_sherpa("Episode 1", "Testing Content")
