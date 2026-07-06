# ============================================================
# Project Name: Microsoft Narrator Compatibility
# ============================================================

# =========================================================
#  DIRECTIONS
# =========================================================
"""
1. Start Chrome with remote debugging enabled:
   chrome.exe --remote-debugging-port=9222

2. Open the example website in that Chrome window.
3. Run this script.
4. Narrator will launch.
5. The script will attach to the already open example tab.
6. Use keyboard arrows, mouse, or standard Narrator controls
   to verify screen reader behavior.
7. Press Enter in the terminal when finished.
"""
# ============================================================
#  Imports
# ============================================================
from playwright.sync_api import sync_playwright
import os
import time
# ============================================================
#                       CONSTANTS
# ============================================================
NARRATOR_PATH = r"C:\Users\benja\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Accessibility\Narrator.lnk"
CHROME_CDP_URL = "http://localhost:9222"
# ============================================================
#                       SOURCE CODE
# ============================================================
def launch_narrator():
    """
    Launch Windows Narrator if available.
    """

    if not os.path.exists(NARRATOR_PATH):
        print(f"Narrator not found at: {NARRATOR_PATH}")
        return False

    os.startfile(NARRATOR_PATH)
    print("Narrator launched. Please confirm activation.")
    time.sleep(2)
    return True

def open_existing_example_page(playwright):
    """
    Connect to an existing Chrome instance via CDP
    and attach to the already open example tab.
    """

    try:
        browser = playwright.chromium.connect_over_cdp(CHROME_CDP_URL)
    except Exception as error:
        raise Exception(
            "Could not connect to Chrome on port 9222. "
            "Make sure Chrome is already running with --remote-debugging-port=9222."
        ) from error

    context_list = browser.contexts

    if not context_list:
        raise Exception("No existing Chrome context was found.")

    chrome_context = context_list[0]

    for page in chrome_context.pages:
        try:
            current_url = page.url.lower()

            if "example.io" in current_url:
                page.bring_to_front()
                print(f"Attached to existing example tab: {page.url}")
                return browser, chrome_context, page
        except Exception:
            continue

    raise Exception("No existing tab was found in the open Chrome window.")
# ============================================================
# Main Function
# ============================================================
def main():
    narrator_started = launch_narrator()

    if not narrator_started:
        print("Narrator failed to start. Aborting test.")
        return

    with sync_playwright() as playwright:
        browser, chrome_context, example_page = open_existing_example_page(playwright)

        print("Existing example tab is ready for manual Narrator testing.")
        input("Press Enter when you are finished testing...")

if __name__ == "__main__":
    main()
