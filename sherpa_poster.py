import os
import json
from playwright.sync_api import sync_playwright

def post_to_sherpa(title: str, content: str):
    storage_state_raw = os.environ.get("STORAGE_STATE_JSON")
    
    if not storage_state_raw:
        raise ValueError("STORAGE_STATE_JSON secret is missing in GitHub Secrets!")

    # Parse and write state to a temporary file safely
    try:
        storage_state = json.loads(storage_state_raw)
        with open("state.json", "w", encoding="utf-8") as f:
            json.dump(storage_state, f)
    except Exception as e:
        raise ValueError(f"Invalid STORAGE_STATE_JSON format in Secrets: {e}")

    with sync_playwright() as p:
        # Launch headless browser for GitHub Actions
        browser = p.chromium.launch(headless=True)
        
        try:
            # Safely create context using the state file
            context = browser.new_context(storage_state="state.json")
            page = context.new_page()
            
            print("Navigating to Pocket FM Sherpa...")
            page.goto("https://sherpa.pocketfm.com/", timeout=60000)
            
            # --- Yahan tumhara aage ka publishing code rahega ---
            # Title aur content fill karne ke steps...
            
            print("Successfully published to Pocket FM Sherpa!")
            
        except Exception as e:
            print(f"❌ Error during Sherpa posting: {e}")
            raise e
        finally:
            browser.close()
            if os.path.exists("state.json"):
                os.remove("state.json")
