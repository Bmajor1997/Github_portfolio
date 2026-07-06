# ==========================================================
# PROJECT NAME: test_semantic_accessibility.py
# ==========================================================

# ==========================================================
# DIRECTIONS
# ==========================================================
"""
Verify the accessibility and semantic accuracy of structural
UI elements, including headings, landmarks,
graphic labels, and error messages, to ensure
they are properly identified, descriptive,
and user-friendly.
"""
# ==========================================================
# IMPORTS
# ==========================================================
import re
from pathlib import Path

import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page
# ==========================================================
# CONSTANTS
# ==========================================================
SCRIBE_URL = "https://test.scribeit.io/"

BASE_DIR = Path(__file__).resolve().parent
STATE = BASE_DIR / "storage_state.json"

GRAPHIC_LABEL_RULES = {
    "image-alt",
    "image-redundant-alt",
    "aria-required-attr",
    "aria-label",
    "aria-labelledby",
}

GENERIC_ERROR_PATTERNS = [
    "error",
    "invalid",
    "something went wrong",
    "malfunction",
    "try again",
    "unknown",
]
# ==========================================================
# AXE HELPERS
# ==========================================================
def run_axe(page: Page) -> list[dict]:
    axe = Axe()
    results = axe.run(page)
    return results.response.get("violations", [])


def check_axe_violations(page: Page) -> None:
    violations = run_axe(page)
    assert not violations, f"Accessibility violations found: {violations}"


def check_graphic_labels(page: Page) -> None:
    violations = run_axe(page)

    graphic_violations = [
        violation
        for violation in violations
        if violation.get("id") in GRAPHIC_LABEL_RULES
    ]

    assert not graphic_violations, f"Graphic label violations found: {graphic_violations}"
# ==========================================================
# HEADING CHECKS
# ==========================================================
def check_headings(page: Page) -> None:
    headings = page.locator(
        "h1:visible, h2:visible, h3:visible, h4:visible, h5:visible, h6:visible"
    ).evaluate_all(
        """
        elements => elements.map((element, index) => ({
            index: index,
            tag: element.tagName.toLowerCase(),
            text: element.innerText.trim(),
            html: element.outerHTML
        }))
        """
    )

    assert headings, "No visible headings found on the page."

    empty_headings = [
        heading
        for heading in headings
        if not heading["text"]
    ]

    if empty_headings:
        print("Empty visible headings found:")
        for heading in empty_headings:
            print(f"Index: {heading['index']}")
            print(f"Tag: {heading['tag']}")
            print(f"HTML: {heading['html']}")

    assert not empty_headings, f"Empty visible headings found: {empty_headings}"

    levels = [
        int(heading["tag"][1])
        for heading in headings
    ]

    assert 1 in levels, f"No visible h1 heading found. Heading levels found: {levels}"

    skipped_levels = []

    for previous, current in zip(levels, levels[1:]):
        if current - previous > 1:
            skipped_levels.append((previous, current))

    assert not skipped_levels, f"Skipped visible heading levels found: {skipped_levels}"
# ==========================================================
# LANDMARK CHECKS
# ==========================================================
def check_landmarks(page: Page) -> None:
    main_landmarks = page.locator("main, [role='main']")
    nav_landmarks = page.locator("nav, [role='navigation']")
    header_landmarks = page.locator("header, [role='banner']")
    footer_landmarks = page.locator("footer, [role='contentinfo']")

    assert main_landmarks.count() > 0, "No main landmark found."
    assert nav_landmarks.count() > 0, "No navigation landmark found."

    print(f"Header landmarks found: {header_landmarks.count()}")
    print(f"Footer landmarks found: {footer_landmarks.count()}")
# ==========================================================
# ERROR MESSAGE CHECKS
# ==========================================================
def check_empty(text: str) -> bool:
    return bool(text and text.strip())


def check_generic(text: str) -> bool:
    if not text or not isinstance(text, str):
        return True

    normalized_text = text.strip().lower()

    for pattern in GENERIC_ERROR_PATTERNS:
        if pattern in normalized_text:
            return True

    if re.fullmatch(r"[\W_]+", normalized_text):
        return True

    return False


def check_error_messages(page: Page) -> None:
    error_elements = page.locator(
        "[role='alert'], "
        "[aria-live='assertive'], "
        "[aria-live='polite'], "
        ".error, "
        "[class*='error'], "
        "[id*='error']"
    )

    error_count = error_elements.count()

    if error_count == 0:
        print("No error messages currently visible on the page.")
        return

    failures = []

    for index in range(error_count):
        error = error_elements.nth(index)

        if not error.is_visible():
            continue

        text = error.inner_text().strip()

        if not check_empty(text):
            failures.append(f"Error message {index} is empty.")

        if check_generic(text):
            failures.append(f"Error message {index} is generic: {text!r}")

    assert not failures, f"Error message issues found: {failures}"
# ==========================================================
# TEST FUNCTION
# ==========================================================
@pytest.mark.browser_context_args(storage_state=str(STATE))
def test_semantic_accessibility(page: Page):
    page.goto(SCRIBE_URL, wait_until="networkidle")

    check_axe_violations(page)
    check_graphic_labels(page)
    check_headings(page)
    check_landmarks(page)
    check_error_messages(page)
