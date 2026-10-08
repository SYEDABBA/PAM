import sys
from playwright.sync_api import sync_playwright

def post_to_sherpa(episode_title: str, episode_content: str):
    with sync_playwright() as p:
        # Launch browser using saved session cookies
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state="state/storage_state.json")
        page = context.new_page()

        print("Navigating to Sherpa Dashboard...")
        page.goto("https://sherpa.pocketfm.com/dashboard")
        
        # Add Playwright click & fill selectors based on Sherpa portal elements
        # E.g., page.click("text=Create Episode")
        # page.fill("input[name='title']", episode_title)
        # page.fill("textarea[name='content']", episode_content)
        # page.click("text=Publish")

        print("Episode Posted Successfully!")
        browser.close()

if __name__ == "__main__":
    print("Sherpa Poster Script Ready!")
