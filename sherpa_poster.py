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
        context = browser.new_context(
            storage_state=state_file,
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print("Navigating to Sherpa Dashboard...")
        page.goto(SHERPA_DASHBOARD, timeout=60000)
        page.wait_for_timeout(4000)

        # Save diagnostic screenshot 1
        page.screenshot(path="step1_dashboard.png")

        print(f"Targeting show URL: {SHOW_URL}")
        page.goto(SHOW_URL, timeout=60000)
        page.wait_for_timeout(5000)

        # Save diagnostic screenshot 2
        page.screenshot(path="step2_showpage.png")

        print("Searching for '+ New episode' button...")
        # Check if button exists
        new_ep_btn = page.get_by_text("+ New episode", exact=False)
        
        if new_ep_btn.count() > 0:
            print("Found button! Clicking now...")
            new_ep_btn.first.click()
            page.wait_for_timeout(4000)
            page.screenshot(path="step3_form.png")

            print("Filling inputs...")
            page.locator("input").first.fill(title)
            page.locator("textarea").first.fill(content)
            page.screenshot(path="step4_filled.png")

            print("Publishing...")
            pub_btn = page.get_by_text("Publish", exact=False)
            if pub_btn.count() > 0:
                pub_btn.first.click()
                page.wait_for_timeout(5000)
                print("Episode published successfully!")
            else:
                print("Publish button not found after filling form.")
        else:
            print("[ERROR] '+ New episode' button not visible on page!")
            page.screenshot(path="error_nobutton.png")
            raise RuntimeError("Automated click failed: '+ New episode' button was not interactable. Check generated screenshots.")

        browser.close()
