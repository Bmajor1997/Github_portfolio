# =============================================================================
# PROJECT NAME: test_keyboard_navigation_validation
# =============================================================================

#=============================================================================
# IMPORTS
#==============================================================================
import random
import time
from pathlib import Path
import pytest
from playwright.sync_api import Page, expect
# =============================================================================
# CONSTANTS
# =============================================================================
DOCS_URL = "https://test.scribeit.io/"
STORAGE_STATE_PATH = Path("storage_state.json")
BASE_DIR = Path(__file__).resolve().parent
TEST_DOCUMENTS_DIR = BASE_DIR / "test_documents" / "PDF"

SAFE_LIMIT = 15
KEYBOARD_TRAP_LIMIT = 20
DROPDOWN_SCROLL_LIMIT = 8
VALID_TARGET_FORMATS = {
    "pdf", "docx", "word", "txt", "html", "epub", "audio", "braille", "daisy"
}

FOCUS_SIGNATURE = """
() => {
    const e = document.activeElement;
    if (!e) return null;

    const text = (e.innerText || e.textContent || "")
        .trim()
        .replace(/\\s+/g, " ")
        .slice(0, 60);

    return {
        tag: e.tagName || "",
        role: e.getAttribute("role") || "",
        id: e.id || "",
        label: e.getAttribute("aria-label") || e.getAttribute("name") || text || "",
        href: e.getAttribute("href") || ""
    };
}
"""

VISIBLE_SIGNATURE = """
() => {
    const e = document.activeElement;
    if (!e) return false;

    const style = window.getComputedStyle(e);
    const rect = e.getBoundingClientRect();

    return (
        style.display !== "none" &&
        style.visibility !== "hidden" &&
        style.opacity !== "0" &&
        rect.width > 0 &&
        rect.height > 0
    );
}
"""
# =============================================================================
# SOURCE CODE
# =============================================================================
def focus_key(focus_obj):
    if not isinstance(focus_obj, dict):
        return str(focus_obj)

    tag = focus_obj.get("tag") or ""
    role = focus_obj.get("role") or ""
    element_id = focus_obj.get("id") or ""
    label = focus_obj.get("label") or ""
    href = focus_obj.get("href") or ""

    key_parts = [
        tag,
        role,
        element_id,
        label,
        href,
    ]

    return "|".join(key_parts)

def focus_readable(focus_obj):
    if not isinstance(focus_obj, dict):
        return str(focus_obj)

    return focus_obj.get("label", "").strip()

def wait_for_page_ready(page: Page, pause_ms=500):

    try:
        page.wait_for_load_state("domcontentloaded", timeout=10000)
    except Exception:
        pass

    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except Exception:
        pass

    page.wait_for_timeout(pause_ms)

def get_test_document():

    print(f"Looking for test documents in: {TEST_DOCUMENTS_DIR.resolve()}")

    if not TEST_DOCUMENTS_DIR.exists():
        raise FileNotFoundError("The test_documents folder does not exist.")

    files = [
        file
        for file in TEST_DOCUMENTS_DIR.rglob("*")
        if file.is_file()
    ]

    if not files:
        raise FileNotFoundError("No test documents found inside test_documents.")

    return files[0]

def upload_test_file(page: Page, file_path):

    resolved_file = str(Path(file_path).resolve())

    file_input = page.locator("input[type='file']").first

    if file_input.count() > 0:
        file_input.set_input_files(resolved_file)
        page.wait_for_timeout(1000)
        return

    with page.expect_file_chooser() as file_chooser_info:
        page.locator("text=Choose File").first.click()

    file_chooser_info.value.set_files(resolved_file)
    page.wait_for_timeout(1000)

def click_start(page: Page):

    start_button = page.get_by_role("button", name="Start")
    start_button.wait_for(state="visible", timeout=10000)
    start_button.click()
    wait_for_page_ready(page, pause_ms=1500)

def wait_for_select_format_ready(page: Page):

    select_format_button = page.get_by_role("button", name="Select Format")

    select_format_button.wait_for(
        state="visible",
    )

    expect(select_format_button).to_be_enabled(
    )

def open_format_dropdown(page: Page):

    dropdown = page.get_by_role("button", name="Select Format")
    dropdown.wait_for(state="visible", timeout=10000)
    dropdown.click()

    page.locator("[role='option'], [role='menuitem']").first.wait_for(
        state="visible",
        timeout=10000
    )

def choose_random_different_format(page: Page, source_extension):

    options = page.locator("[role='option'], [role='menuitem'], li, button")
    valid_options = []

    for index in range(options.count()):
        option = options.nth(index)
        option_text = option.inner_text().strip()

        normalized_option = option_text.lower()
        normalized_source = source_extension.lower().replace(".", "")

        if normalized_option in VALID_TARGET_FORMATS and normalized_option != normalized_source:
            valid_options.append((option, option_text))

    if not valid_options:
        raise Exception("No valid target formats were found in the dropdown.")

    chosen_option, chosen_text = random.choice(valid_options)
    chosen_option.click()

    return chosen_text

def wait_for_converted_output_ready(page: Page, timeout_ms=60000):

    start_time = time.time()

    while time.time() - start_time < timeout_ms / 1000:
        try:
            page_text = page.locator("body").inner_text(timeout=3000)

            if "Processing..." not in page_text:
                page.wait_for_timeout(1500)
                return

        except Exception:
            pass

        page.wait_for_timeout(500)

    raise TimeoutError("Converted output did not finish processing.")

def click_convert(page: Page):

    convert_button = page.get_by_role("button", name="Convert", exact=True)
    convert_button.wait_for(state="visible", timeout=10000)
    convert_button.click()

    wait_for_page_ready(page, pause_ms=2000)
    wait_for_converted_output_ready(page)

def check_tab_navigation(page: Page, limit=SAFE_LIMIT):
    seen_keys = []

    page.focus("body")

    for attempt in range(limit):
        before = page.evaluate(FOCUS_SIGNATURE)
        before_key = focus_key(before)

        page.keyboard.press("Tab")
        page.wait_for_timeout(100)

        after = page.evaluate(FOCUS_SIGNATURE)
        after_key = focus_key(after)

        if after_key == before_key:
            raise Exception(
                "Possible keyboard trap because focus did not move."
            )

        if after_key in seen_keys[-3:]:
            raise Exception(
                "Possible keyboard trap because focus repeated."
            )

        seen_keys.append(after_key)

    return seen_keys

def check_shift_tab_navigation(page: Page, limit=SAFE_LIMIT):

    seen_keys = []

    page.focus("body")

    for attempt in range(limit):
        before = page.evaluate(FOCUS_SIGNATURE)
        before_key = focus_key(before)

        page.keyboard.press("Shift+Tab")
        page.wait_for_timeout(100)

        after = page.evaluate(FOCUS_SIGNATURE)
        after_key = focus_key(after)

        if after_key == before_key:
            raise Exception(
                "Possible keyboard trap because focus did not move."
            )

        if after_key in seen_keys[-3:]:
            raise Exception(
                "Possible keyboard trap because focus repeated."
            )

        seen_keys.append(after_key)

    return seen_keys

def check_keyboard_trap(page: Page, limit=KEYBOARD_TRAP_LIMIT):

    tab_history = check_tab_navigation(page)
    shift_tab_history = check_shift_tab_navigation(page)

    combined_history = tab_history + shift_tab_history

    if len(combined_history) != len(set(combined_history)):
        raise Exception(
            "Possible keyboard trap because focus repeated during keyboard navigation."
        )

    return {
        "tab_history": tab_history,
        "shift_tab_history": shift_tab_history,
    }
    
def check_dropdown_arrow_navigation(page: Page):

    page.keyboard.press("Home")
    page.wait_for_timeout(200)

    moved_down = False
    moved_up = False

    for _ in range(DROPDOWN_SCROLL_LIMIT):
        before = focus_readable(page.evaluate(FOCUS_SIGNATURE))

        page.keyboard.press("ArrowDown")
        page.wait_for_timeout(50)

        after = focus_readable(page.evaluate(FOCUS_SIGNATURE))

        if after != before:
            moved_down = True

    for _ in range(DROPDOWN_SCROLL_LIMIT):
        before = focus_readable(page.evaluate(FOCUS_SIGNATURE))

        page.keyboard.press("ArrowUp")
        page.wait_for_timeout(50)

        after = focus_readable(page.evaluate(FOCUS_SIGNATURE))

        if after != before:
            moved_up = True

    if not moved_down:
        raise Exception("Dropdown did not move downward with ArrowDown.")

    if not moved_up:
        raise Exception("Dropdown did not move upward with ArrowUp.")

    return
# =============================================================================
# TEST FUNCTION
# =============================================================================
@pytest.mark.browser_context_args(storage_state=str(STORAGE_STATE_PATH))
def test_keyboard_navigation_accessibility(page: Page):

    test_document = get_test_document()
    source_extension = test_document.suffix.lower().replace(".", "")

    page.goto(DOCS_URL, wait_until="networkidle")
    wait_for_page_ready(page)

    page.locator("body").click()
    page.keyboard.press("Home")

    check_tab_navigation(page)
    check_shift_tab_navigation(page)
    check_keyboard_trap(page)

    page.goto("https://test.scribeit.io/", wait_until="networkidle")
    wait_for_page_ready(page)

    upload_test_file(page, test_document)
    click_start(page)

    wait_for_select_format_ready(page)

    open_format_dropdown(page)

    check_dropdown_arrow_navigation(page)

    choose_random_different_format(page, source_extension)

    click_convert(page)
