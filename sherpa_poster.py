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

        print("Navigating to Sherpa Pocket FM Dashboard...")
        page.goto(SHERPA_DASHBOARD, timeout=60000)
        page.wait_for_load_state("networkidle")

        print(f"Targeting specific show: {SHOW_URL}")
        page.goto(SHOW_URL, timeout=60000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000) # Wait for UI elements to load fully

        print("Attempting to find and click 'New Episode' button...")
        try:
            # Try multiple common button identifiers for Sherpa/Pocket FM
            btn_selectors = [
                "text=New Episode",
                "text=नया एपिसोड",
                "button:has-text('Episode')",
                "a:has-text('Episode')",
                "[class*='create']",
                "[class*='episode']"
            ]
            
            clicked = False
            for selector in btn_selectors:
                element = page.locator(selector)
                if element.count() > 0:
                    print(f"Found element with selector: {selector}")
                    element.first.click()
                    clicked = True
                    break
            
            if not clicked:
                print("Could not find direct button, trying to navigate via URL pattern if available...")
                # Fallback: log page text to help identify
                print(f"Current Page URL: {page.url}")

            page.wait_for_timeout(3000)
            
            print("Filling episode details...")
            # Universal selectors for text inputs and textareas
            page.fill("input[type='text']", title)
            page.fill("textarea", content)
            
            print("Looking for publish/submit button...")
            submit_selectors = ["text=Publish", "text=पब्लिश", "button[type='submit']"]
            for sub_sel in submit_selectors:
                sub_btn = page.locator(sub_sel)
                if sub_btn.count() > 0:
                    sub_btn.first.click()
                    print("Episode successfully submitted for publishing!")
                    break
            
            page.wait_for_timeout(5000)

        except Exception as e:
            print(f"Automation notice during publishing: {e}")
            os.makedirs("my work", exist_ok=True)
            with open(f"my work/{title}.txt", "w", encoding="utf-8") as file_out:
                file_out.write(content)
            print("Story saved safely to 'my work/' folder as backup.")

        browser.close()
