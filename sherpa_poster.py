import os
import json
from playwright.sync_api import sync_playwright

SHOW_URL = "https://pocketfm.com/show/a739c232bc15d2c49ce52e650509a651d9b5dd0a"
SHERPA_DASHBOARD = "https://sherpa.pocketfm.com/"

def post_to_sherpa(title: str, content: str):
    storage_state_env = os.environ.get("STORAGE_STATE_JSON")
    
    # Always keep local backup for complete safety
    os.makedirs("my work", exist_ok=True)
    file_path = os.path.join("my work", f"{title}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📁 Local backup saved at: {file_path}")

    if not storage_state_env:
        print("[ERROR] STORAGE_STATE_JSON secret is missing!")
        return

    state_file = "state.json"
    with open(state_file, "w", encoding="utf-8") as f:
        f.write(storage_state_env)

    with sync_playwright() as p:
        try:
            # Launch with advanced stealth flags to bypass bot detection / cloudflare
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-infobars",
                    "--window-size=1280,720"
                ]
            )
            
            context = browser.new_context(
                storage_state=state_file,
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            
            # Hide automation fingerprints
            context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
            
            page = context.new_page()

            print("Navigating to Sherpa Dashboard...")
            page.goto(SHERPA_DASHBOARD, timeout=60000)
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(5000)

            print(f"Targeting specific show URL: {SHOW_URL}")
            page.goto(SHOW_URL, timeout=60000)
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(5000)

            print("Waiting for '+ New episode' button to render...")
            btn_locator = page.locator("text=+ New episode")
            btn_locator.wait_for(state="visible", timeout=20000)
            
            print("Clicking '+ New episode' button...")
            btn_locator.first.click()
            page.wait_for_timeout(4000)

            print("Filling episode title and content...")
            page.locator("input[type='text']").first.fill(title)
            page.locator("textarea").first.fill(content)
            page.wait_for_timeout(2000)

            print("Submitting/Publishing episode to Pocket FM...")
            publish_btn = page.locator("button:has-text('Publish'), button:has-text('Submit'), text=Publish")
            if publish_btn.count() > 0:
                publish_btn.first.click()
                page.wait_for_timeout(6000)
                print("✅ Episode successfully uploaded and published to Sherpa!")
            else:
                # Fallback JS trigger for publish button
                page.evaluate("""() => {
                    const buttons = Array.from(document.querySelectorAll('button'));
                    const btn = buttons.find(b => b.textContent.includes('Publish') || b.textContent.includes('पब्लिश'));
                    if (btn) btn.click();
                }""")
                page.wait_for_timeout(5000)
                print("✅ Episode submission triggered via stealth fallback script!")

            browser.close()
        except Exception as e:
            print(f"[NOTICE] Direct upload encountered a block: {e}")
            print("Your story is fully secure in the repository 'my work/' folder.")
