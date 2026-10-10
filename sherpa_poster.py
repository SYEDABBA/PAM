import os
import json
from playwright.sync_api import sync_playwright

SHOW_URL = "https://pocketfm.com/show/a739c232bc15d2c49ce52e650509a651d9b5dd0a"
SHERPA_DASHBOARD = "https://sherpa.pocketfm.com/"

def post_to_sherpa(title: str, content: str):
    storage_state_env = os.environ.get("STORAGE_STATE_JSON")
    
    # Always save locally as primary safety backup
    os.makedirs("my work", exist_ok=True)
    file_path = os.path.join("my work", f"{title}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📁 Story successfully saved locally at: {file_path}")

    if not storage_state_env:
        print("[WARNING] STORAGE_STATE_JSON secret is missing.")
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
            page.goto(SHERPA_DASHBOARD, timeout=50000)
            page.wait_for_timeout(4000)

            print(f"Targeting show URL: {SHOW_URL}")
            page.goto(SHOW_URL, timeout=50000)
            page.wait_for_timeout(6000)

            print("Attempting to trigger '+ New episode' via JavaScript...")
            # JavaScript evaluation to find and click the button containing "+ New episode"
            clicked = page.evaluate("""() => {
                const buttons = Array.from(document.querySelectorAll('button, div, span, a'));
                const target = buttons.find(el => el.textContent && el.textContent.includes('+ New episode'));
                if (target) {
                    target.click();
                    return true;
                }
                return false;
            }""")

            if clicked:
                print("Successfully clicked 'New Episode' button via JS!")
                page.wait_for_timeout(4000)

                print("Filling title and content...")
                page.locator("input[type='text']").first.fill(title)
                page.locator("textarea").first.fill(content)
                page.wait_for_timeout(2000)

                print("Submitting episode...")
                page.evaluate("""() => {
                    const buttons = Array.from(document.querySelectorAll('button'));
                    const pubBtn = buttons.find(el => el.textContent && el.textContent.toLowerCase().includes('publish'));
                    if (pubBtn) {
                        pubBtn.click();
                        return true;
                    }
                    return false;
                }""")
                page.wait_for_timeout(5000)
                print("Episode submission command executed!")
            else:
                print("[INFO] Could not locate New Episode button automatically. Saved locally for easy manual push.")

            browser.close()
        except Exception as e:
            print(f"[NOTICE] Automation execution note: {e}")
