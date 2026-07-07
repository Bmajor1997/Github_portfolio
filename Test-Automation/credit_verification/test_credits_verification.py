# =============================================================================
# PROJECT NAME: test_credits_verification
# =============================================================================
 
# =============================================================================
# DIRECTIONS
# =============================================================================
"""
Open ScribeIt, navigate to the appropriate page, retrieve the current credits count from the page content,
and display the extracted value.
"""
# =============================================================================
# IMPORTS
# =============================================================================
import re
import pytest
from pathlib import Path
# =============================================================================
# CONSTANTS
# =============================================================================
SCRIBE_URL = "https://test.scribeit.io/"
CREDITS_SELECTOR = None  # set to a string selector when you have it
BASE_DIR = Path(__file__).resolve().parent
STATE = BASE_DIR / "storage_state.json"
# =============================================================================
# SOURCE CODE
# =============================================================================
def extract_credits_best_effort(text: str) -> int | None:
    """
    Best-effort extraction:
    1) Prefer patterns near the word 'credit(s)'
    2) Fall back to a plausible standalone number (2-6 digits, allowing commas)
    """
    t = text or ""

    # Prefer "2430 credits" / "credits 2430" / "2,430 Credits"
    m = re.search(r"\b(\d{1,6}(?:,\d{3})*)\s*credits?\b", t, re.I)
    if not m:
        m = re.search(r"\bcredits?\s*(\d{1,6}(?:,\d{3})*)\b", t, re.I)
    if m:
        return int(m.group(1).replace(",", ""))

    # Fallback: first plausible larger number (avoid tiny numbers like 1, 2, 3)
    m2 = re.search(r"\b\d{2,6}(?:,\d{3})*\b", t)
    if m2:
        return int(m2.group(0).replace(",", ""))

    return None

def get_best_context(browser):
    if not browser.contexts:
        raise RuntimeError("No browser contexts found via CDP. Is Chrome running with --remote-debugging-port=9222?")
    return browser.contexts[0]

def get_or_create_page(context):
    return context.pages[0] if context.pages else context.new_page()

def read_credits(page) -> int | None:
    page.goto(SCRIBE_URL, wait_until="networkidle")
    page.wait_for_timeout(1500)  # small buffer for dynamic UI

    # If you have a known selector, use it first (most accurate)
    if isinstance(CREDITS_SELECTOR, str) and CREDITS_SELECTOR.strip():
        loc = page.locator(CREDITS_SELECTOR).first
        if loc.count() > 0:
            txt = (loc.inner_text() or "").strip()
            got = extract_credits_best_effort(txt)
            if got is not None:
                return got

    # Fallback: scan visible body text
    body = page.locator("body").inner_text() or ""
    return extract_credits_best_effort(body)
# =============================================================================
# TEST FUNCTION
# =============================================================================
@pytest.mark.browser_context_args(storage_state=str(STATE))
def test_number_of_credits_verifier(page):

    credits = read_credits(page)

    assert credits is not None, "Could not find credits count on the ScribeIt page."

    print(f"Current credits count: {credits}")
