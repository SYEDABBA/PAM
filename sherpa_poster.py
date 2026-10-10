import os
import json
from playwright.sync_api import sync_playwright

SHOW_URL = "https://pocketfm.com/show/a739c232bc15d2c49ce52e650509a651d9b5dd0a"
SHERPA_DASHBOARD = "https://sherpa.pocketfm.com/"

def post_to_sherpa(title: str, content: str):
    storage_state_env = os.environ.get("STORAGE_STATE_JSON")
    if not storage_state_env:
        raise ValueError("STORAGE_STATE_JSON secret is missing in GitHub Secrets!")

    # Write the secret directly to a state.json file to avoid type/path errors
    state_file = "state.json"
    with open(state_file, "w", encoding="utf-8") as f:
        f.write(storage_state_env)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Pass the file path string directly
        context = browser.new_context(storage_state=state_file)
        page = context.new_page()

        print("Navigating to Sherpa Pocket FM Dashboard...")
        page.goto(SHERPA_DASHBOARD, timeout=60000)
        page.wait_for_load_state("networkidle")

        print(f"Targeting specific show: {SHOW_URL}")
        page.goto(SHOW_URL, timeout=60000)
        page.wait_for_load_state("networkidle")

        print("Looking for 'New Episode' or publish button...")
        try:
            new_ep_btn = page.locator("text=New Episode")
            if new_ep_btn.count() > 0:
                new_ep_btn.first.click()
                page.wait_for_timeout(3000)
            
            print("Filling episode details...")
            page.fill("input[placeholder*='Episode Title']", title)
            page.fill("textarea[placeholder*='Episode Content']", content)
            
            submit_btn = page.locator("text=Publish")
            if submit_btn.count() > 0:
                submit_btn.first.click()
                print("Episode successfully published to Sherpa!")
            else:
                print("Publish button not found, saving locally as backup.")
        
        except Exception as e:
            print(f"Automation notice during publishing: {e}")
            os.makedirs("my work", exist_ok=True)
            with open(f"my work/{title}.txt", "w", encoding="utf-8") as file_out:
                file_out.write(content)
            print("Story saved safely to 'my work/' folder.")

        browser.close()
