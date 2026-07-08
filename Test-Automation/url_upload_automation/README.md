## Project Overview

URL Upload Automation demonstrates an automated approach to validating a document upload workflow using a web URL instead of a local file. Built with Python and Playwright, this project verifies that a user can submit a supported document URL, start processing, select an output format, and complete the conversion workflow.

This project supports quality assurance by reducing repetitive manual validation and creating a repeatable end-to-end test for a key document processing feature.

## Why I Built This

URL-based document upload workflows can involve multiple steps, including entering a document URL, starting processing, waiting for the system to analyze the file, selecting an output format, and completing conversion.

I built this automation to validate that workflow consistently and reduce the amount of manual effort needed to confirm that URL uploads function correctly.

## Project Objectives

- Validate document upload using a URL.
- Verify that the application accepts a supported document link.
- Confirm processing begins after submission.
- Validate output format selection.
- Complete the conversion workflow.
- Create a repeatable end-to-end automation test.

## How It Works

The automation follows a structured testing workflow:

1. Open the target web application.
2. Select the URL upload option.
3. Enter a supported document URL.
4. Start the upload and processing workflow.
5. Wait for the document processing state to complete.
6. Select the desired output format.
7. Complete the conversion process.
8. Validate that the workflow reaches the expected result.

The following example demonstrates the core URL upload workflow, including entering the document URL, starting processing, validating the processing message, selecting the output format, and confirming the document is ready.

```python
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

select_format_button = page.get_by_role("button", name="Select Format")
expect(select_format_button).to_be_visible()
expect(select_format_button).to_be_enabled()

select_format_button.click()

```
## Full Implementation

The complete implementation of this project, including URL submission, processing validation, format selection, and conversion workflow automation, is available in:

➡️ [`url_upload_automation.py`](test_upload_using_url.py)

## Technologies Used

- Python
- Playwright
- Pytest
- Git
- GitHub
- url link
  
## Skills Demonstrated

- End-to-End Test Automation
- Playwright Automation
- Python Development
- URL Upload Validation
- Workflow Testing
- UI Interaction Testing
- Synchronization and Wait Handling
- Software Quality Assurance

## Challenges and Lessons Learned

Developing this automation reinforced the importance of reliable synchronization when testing workflows that depend on processing states, dynamic UI updates, and conditional elements. It also strengthened my understanding of how to break a larger user workflow into reusable helper functions that are easier to maintain and debug.

## Future Improvements

- Add HTML reporting for test results.
- Expand validation for additional supported URL document types.
- Add negative testing for invalid or unsupported URLs.
- Improve reusable helper functions for broader workflow coverage.
- Integrate automated execution through GitHub Actions.


