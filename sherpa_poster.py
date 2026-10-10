import os
import json
from playwright.sync_api import sync_playwright

SHOW_URL = "https://pocketfm.com/show/a739c232bc15d2c49ce52e650509a651d9b5dd0a"
SHERPA_DASHBOARD = "https://sherpa.pocketfm.com/"

def post_to_sherpa(title: str, content: str):
    storage_state_env = os.environ.get("STORAGE_STATE_JSON")
    if not storage_state_env:
        raise ValueError("STORAGE_STATE_JSON secret is missing in GitHub Secrets!")

    # Parse cookies/storage state from GitHub secret
    storage_state = json.loads(storage_state_env)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=storage_state)
        page = context.new_page()

        print("Navigating to Sherpa Pocket FM Dashboard...")
        page.goto(SHERPA_DASHBOARD, timeout=60000)
        page.wait_for_load_state("networkidle")

        # Directly navigate to the specific show page
        print(f"Targeting specific show: {SHOW_URL}")
        page.goto(SHOW_URL, timeout=60000)
        page.wait_for_load_state("networkidle")

        print("Looking for 'New Episode' or publish button...")
        try:
            # Click on new episode button (adjust selector based on Sherpa UI)
            new_ep_btn = page.locator("text=New Episode")
            if new_ep_btn.count() > 0:
                new_ep_btn.first.click()
                page.wait_for_timeout(3000)
            
            # Fill title and content fields
            print("Filling episode details...")
            page.fill("input[placeholder*='Episode Title']", title)
            page.fill("textarea[placeholder*='Episode Content']", content)
            
            # Click publish/submit
            submit_btn = page.locator("text=Publish")
            if submit_btn.count() > 0:
                submit_btn.first.click()
                print("Episode successfully published to Sherpa!")
            else:
                print("Publish button not found, saving as draft/manual review required.")
        
        except Exception as e:
            print(f"Automation notice during publishing: {e}")
            # Fallback: save content locally if UI changes
            os.makedirs("my work", exist_ok=True)
            with open(f"my work/{title}.txt", "w", encoding="utf-8") as f:
                f.write(content)
            print("Story saved safely to 'my work/' folder.")

        browser.close()
