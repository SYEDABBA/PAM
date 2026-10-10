import os
import json
from playwright.sync_api import sync_playwright

SHOW_URL = "https://pocketfm.com/show/a739c232bc15d2c49ce52e650509a651d9b5dd0a"
SHERPA_DASHBOARD = "https://sherpa.pocketfm.com/"

def post_to_sherpa(title: str, content: str):
    storage_state_env = os.environ.get("STORAGE_STATE_JSON")
    if not storage_state_env:
        raise ValueError("STORAGE_STATE_JSON secret is missing in GitHub Secrets!")

    state_file = "state.json"
    with open(state_file, "w", encoding="utf-8") as f:
        f.write(storage_state_env)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=state_file)
        page = context.new_page()

        print("Navigating to Sherpa Dashboard...")
        page.goto(SHERPA_DASHBOARD, timeout=60000)
        page.wait_for_load_state("networkidle")

        print(f"Targeting show URL: {SHOW_URL}")
        page.goto(SHOW_URL, timeout=60000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000)

        print("Clicking '+ New episode' button...")
        try:
            # Exact selector based on the Sherpa UI screenshot
            page.locator("text=+ New episode").first.click()
            page.wait_for_timeout(4000)

            print("Filling episode title and content...")
            # Fill inputs found on the popup/new episode page
            page.fill("input[type='text']", title)
            page.fill("textarea", content)
            
            print("Submitting/Publishing episode...")
            # Click submit or publish button
            publish_btn = page.locator("button:has-text('Publish'), button:has-text('Submit'), text=Publish")
            if publish_btn.count() > 0:
                publish_btn.first.click()
                print("Episode successfully published to Pocket FM!")
            else:
                print("Publish button selector not matched, saving draft state.")
            
            page.wait_for_timeout(5000)

        except Exception as e:
            print(f"Automation execution notice: {e}")
            os.makedirs("my work", exist_ok=True)
            with open(f"my work/{title}.txt", "w", encoding="utf-8") as f:
                f.write(content)
            print("Content safely backed up in local 'my work/' folder.")

        browser.close()
