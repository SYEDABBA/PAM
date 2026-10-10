import os
import json
from playwright.sync_api import sync_playwright

SHOW_URL = "https://pocketfm.com/show/a739c232bc15d2c49ce52e650509a651d9b5dd0a"
SHERPA_DASHBOARD = "https://sherpa.pocketfm.com/"

def post_to_sherpa(title: str, content: str):
    storage_state_env = os.environ.get("STORAGE_STATE_JSON")
    
    # Save content locally first as primary/backup mechanism
    os.makedirs("my work", exist_ok=True)
    file_path = os.path.join("my work", f"{title}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📁 Story successfully saved locally at: {file_path}")

    if not storage_state_env:
        print("[WARNING] STORAGE_STATE_JSON secret is missing. Skipping browser automation.")
        return

    state_file = "state.json"
    with open(state_file, "w", encoding="utf-8") as f:
        f.write(storage_state_env)

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                storage_state=state_file,
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            print("Navigating to Sherpa Dashboard...")
            page.goto(SHERPA_DASHBOARD, timeout=40000)
            page.wait_for_timeout(3000)

            print(f"Targeting show URL: {SHOW_URL}")
            page.goto(SHOW_URL, timeout=40000)
            page.wait_for_timeout(4000)

            new_ep_btn = page.get_by_text("+ New episode", exact=False)
            if new_ep_btn.count() > 0:
                print("Found button! Clicking...")
                new_ep_btn.first.click()
                page.wait_for_timeout(3000)

                print("Filling inputs...")
                page.locator("input").first.fill(title)
                page.locator("textarea").first.fill(content)

                print("Publishing...")
                pub_btn = page.get_by_text("Publish", exact=False)
                if pub_btn.count() > 0:
                    pub_btn.first.click()
                    page.wait_for_timeout(4000)
                    print("Episode successfully published to Pocket FM via automation!")
            else:
                print("[INFO] Dashboard login state might need a refresh. Story is safely saved locally in 'my work/' for quick posting.")

            browser.close()
        except Exception as e:
            print(f"[NOTICE] Browser automation skipped due to network/auth state: {e}")
            print("Your generated story is completely safe in the repository files.")
