# ======================================
#  NAME: test_upload_using_url.py
# ======================================

#====================================
#   DIRECTIONS
#=====================================
"""
Automate an example website Upload using URL workflow by submitting a document URL,
selecting the HTML "Read full version in browser" format after processing completes,
and converting the document once the selected format is ready.
"""
#====================================
#   IMPORTS
#=====================================
from pathlib import Path
import re
import pytest
from playwright.sync_api import Page, expect
#====================================
#   CONSTANTS
#=====================================
BASE_DIR = Path(__file__).resolve().parent
STATE = BASE_DIR / "storage_state.json"
HOME_URL = "https://Example.io/"
DOCUMENT_URL = "https://www.orimi.com/pdf-test.pdf"
TIMEOUT_SECONDS = 60
#====================================
#  SOURCE CODE
#=====================================
@pytest.mark.browser_context_args(storage_state=str(STATE))
def test_upload_using_url(page: Page):
    page.set_default_timeout(300000)
    expect.set_options(timeout=300000)

    page.goto(HOME_URL, wait_until="domcontentloaded")

    url_box = page.locator("#form_url")
    expect(url_box).to_be_visible()

    url_box.fill(DOCUMENT_URL)

    assert url_box.input_value() == DOCUMENT_URL, (
        "URL field was not filled correctly."
    )

    start_button = page.get_by_role("button", name="Start")
    expect(start_button).to_be_visible()
    expect(start_button).to_be_enabled()

    start_button.click()

    page_count_message = page.get_by_text(
        re.compile(r"This document has \d+ page[s]?\.", re.IGNORECASE)
    )
    expect(page_count_message).to_be_visible()

    process = page.get_by_text("Processing...", exact=True)
    expect(process).to_be_visible()

    select_format_button = page.get_by_role(
        "button",
        name="Select Format"
    )

    expect(select_format_button).to_be_visible()
    expect(select_format_button).to_be_enabled()

    select_format_button.click()

    html_format_option = page.get_by_text(
        "Read full version in browser",
        exact=True
    )

    expect(html_format_option).to_be_visible()

    html_format_option.click()

    selected_format_heading = page.get_by_role(
        "heading",
        name="Read full version in browser"
    )

    expect(selected_format_heading).to_be_visible()

    convert_button = page.get_by_role(
        "button",
        name="Convert",
        exact=True
    )

    expect(convert_button).to_be_visible()
    expect(convert_button).to_be_enabled()

    convert_button.click()

    document_ready_message = page.get_by_text(
        "Document ready.",
        exact=False
    )

    expect(document_ready_message).to_be_visible()

    output_link = page.get_by_role("link", name="Document", exact=False)
    expect(output_link).to_be_visible()
