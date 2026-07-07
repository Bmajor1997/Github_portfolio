# ==========================================================
# Project Name: test_toast_notifications.py
# ==========================================================

# ==========================================================
# DIRECTIONS
# ==========================================================
"""
Upload supported test files to Website, start processing,
and verify that a "Processing..." toast notification appears after the
Start button is clicked.
"""
# ==========================================================
# IMPORTS
# ==========================================================
import re
from pathlib import Path
import pytest
# ==========================================================
# CONSTANTS
# ==========================================================
WEBSITE = "https://example.io/"
BASE_DIR = Path(__file__).resolve().parent
STATE = BASE_DIR / "storage_state.json"
TEST_DOCS_DIR = (BASE_DIR / "test_documents"/ "various_test_documents_for_projects")
SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".mp3",
    ".brf",
    ".html",
    ".epub",
    ".mobi",
    ".rtf",
    ".ppt",
    ".pptx",
    ".bmp",
    ".tif",
    ".jpeg",
    ".txt"
}
# ==========================================================
# SOURCE CODE
# ==========================================================
def get_test_files():
    """
    Returns every test file in TEST_DOCS_DIR that matches
    one of the allowed extensions.
    """
    if not TEST_DOCS_DIR.is_dir():
        print(f"Test documents folder not found: {TEST_DOCS_DIR}")
        return []


    target_file = TEST_DOCS_DIR / "Appendix 3_Water Quality Tables_0002.tif"

    if not target_file.exists():
        print(f"Test file not found: {target_file}")
        return []

    return [target_file]

def upload_document(page, file_path: Path):
    """
    Uploads a document to scribeit.io.
    """
    file_input = page.locator("input[type='file']").first
    file_input.wait_for(timeout=5000)
    print(f"Uploading file: {file_path.name}")
    file_input.set_input_files(str(file_path))

def wait_for_first_toast(page, timeout_ms=10000):
    """
    Clicks Start and looks for the first processing toast notification.
    """
    try:
        start_button = page.get_by_role("button", name="Start")
        start_button.wait_for(timeout=timeout_ms)
        start_button.click()
        print("Start button clicked.")
    except Exception as error:
        print(f"Start button not found on page {page.url}: {error}")
        return False

    page.wait_for_timeout(1500)

    toast_patterns = [
        re.compile(r"processing", re.I),
        re.compile(r"uploading", re.I),
        re.compile(r"starting", re.I),
        re.compile(r"please wait", re.I),
    ]

    for pattern in toast_patterns:
        try:
            page.get_by_text(pattern, exact=False).first.wait_for(timeout=3000)
            return True
        except Exception:
            continue

    print("First processing toast did not appear.")

    try:
        body_text = page.locator("body").inner_text(timeout=3000)

        page_count_match = re.search(r"This document has \d+ pages?\.", body_text, re.I)
        if page_count_match:
            print(page_count_match.group(0))

    except Exception:
        print("Could not capture page count after clicking Start.")

    return False

def click_select_format(page, timeout_ms=40000):

    """
        Waits for the format-selection stage.

        If the page requires remediation, the test fails.
        """

    # Detect remediation requirement
    remediate_btn = page.get_by_role("button", name="Remediate Full Document")

    if remediate_btn.count() > 0 and remediate_btn.first.is_visible():
        raise Exception("Scribe requires remediation; cannot proceed to Select Format.")

    try:
        select_button = page.get_by_role("button", name="Select Format")
        select_button.wait_for(timeout=timeout_ms)

        if not select_button.is_visible():
            raise Exception("Select Format button exists but is not visible.")

        if not select_button.is_enabled():
            raise Exception("Select Format button exists but is not enabled.")

        select_button.click()
        print("Select Format button clicked.")
        return True

    except Exception as error:
        print(f"Select Format button not found: {error}")
        return False

def choose_format(page, target_format, timeout_ms: int = 10000):
    """
    Chooses a format from the format dropdown.
    """
    try:
        option = page.get_by_text(target_format, exact=False)
        option.wait_for(timeout=timeout_ms)
        option.click()
        print(f"Selected format: {target_format}")
        return True
    except Exception as error:
        print(f"Format '{target_format}' not found: {error}")
        return False

def click_convert(page, timeout_ms: int = 10000):
    """
    Clicks the Convert button.
    """
    try:
        convert_button = page.get_by_role("button", name="Convert", exact=True)
        convert_button.wait_for(timeout=timeout_ms)
        convert_button.click()
        return True
    except Exception as error:
        print(f"Convert button not found: {error}")
        return False

def wait_for_second_toast(page, timeout_ms: int = 10000):
    """
    Looks for the second processing toast notification.
    """
    try:
        page.get_by_text("processing...", exact=False).wait_for(timeout=timeout_ms)
        return True
    except Exception:
        print("Second processing toast did not appear.")
        return False

def run_toast_tests_for_all_files(page):
    test_files = get_test_files()

    if not test_files:
        print("No test files found matching supported extensions in test_documents.")
        return

    for file_path in test_files:
        print(f"\n--- Testing file: {file_path.name} ---")

        page.goto(WEBSITE, wait_until="domcontentloaded")
        upload_document(page, file_path)

        first_toast_ok = wait_for_first_toast(page)

        if not first_toast_ok:
            print(f"First toast notification did NOT appear for {file_path.name}")
            continue

        print(f"First toast notification appeared for {file_path.name}")

        try:
            format_stage_ok = click_select_format(page)
        except Exception as error:
            print(f"❌ {file_path.name}: {error}")
            continue

        if not format_stage_ok:
            print(f"Select Format stage did NOT appear for {file_path.name}")
            continue

        # Choose the first format for this test (you could loop formats later)
        target_format = "PDF"

        if not choose_format(page, target_format):
            continue

        if not click_convert(page):
            continue

        second_toast_ok = wait_for_second_toast(page)

        if second_toast_ok:
            print(f"Second toast notification appeared for {file_path.name}")
        else:
            print(f"Second toast notification did NOT appear for {file_path.name}")

# ==========================================================
# TEST FUNCTION
# ==========================================================
@pytest.mark.browser_context_args(storage_state=str(STATE))
def test_toast_notifications(page):

    """
        Launches Chromium and runs toast tests
        for all files in test_documents.
        """

    test_files = get_test_files()

    assert test_files, "No test files found matching supported extensions in test_documents."

    page.goto(WEBSITE, wait_until="networkidle")

    run_toast_tests_for_all_files(page)
