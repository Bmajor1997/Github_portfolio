## Project Overview

Toast Notification Validation demonstrates an automated approach to validating application workflow feedback through transient toast notifications using Python and Playwright. Rather than validating notifications in isolation, the project uses toast messages as checkpoints to verify that key stages of a document conversion workflow progress successfully.

By combining workflow automation with dynamic notification validation, the project creates a repeatable method for confirming application state changes and user feedback throughout the conversion process.

---

## Why I Built This

Toast notifications are commonly used to communicate the success, failure, or progress of user actions. Because these notifications appear dynamically and often disappear after a short period, they can be challenging to validate consistently through manual testing.

I developed this automation to create a repeatable process for validating notification visibility, message content, and timing during end-to-end application workflows.

---

## Project Objectives

- Validate toast notification visibility.
- Verify notification message accuracy.
- Confirm notifications appear at the correct point in the workflow.
- Ensure notifications remain visible long enough for validation.
- Create a reusable workflow for dynamic UI validation.

## How it Works

1. Load the target application.
2. Retrieve the supported test file.
3. Upload the document.
4. Click Start.
5. Check for the first processing-related toast.
6. Wait for the Select Format stage.
7. Select PDF as the target format.
8. Click Convert.
9. Check for the second processing toast.
10. Print workflow results.

The following example demonstrates the core URL upload workflow, including entering the document URL, starting processing, validating the processing message, selecting the output format, and confirming the document is ready.

```python
def wait_for_first_toast(page, timeout_ms=10000):
    """
    Clicks Start and looks for the first processing toast notification.
    """
    try:
        start_button = page.get_by_role("button", name="Start")
        start_button.wait_for(timeout=timeout_ms)
        start_button.click()
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

    return False
   ```
 ## Full Implementation

The complete implementation of this project, including toast notification detection, visibility validation, synchronization logic, and workflow verification, is available in:

➡️ [`toast_notification_validation.py`](test_toast_notification.py)

## Technologies Used

- Python
- Playwright
- Pytest
- Git
- GitHub

---

## Skills Demonstrated

- Test Automation
- Dynamic UI Validation
- Playwright Automation
- Python Development
- Synchronization Strategies
- Explicit Waiting
- End-to-End Testing
- Software Quality Assurance

---

## Challenges and Lessons Learned

Developing this project reinforced the importance of synchronizing automation with dynamic application behavior. Rather than relying on fixed messages, the automation was designed to recognize multiple valid notification patterns while continuing to verify workflow progression.

The project also strengthened my understanding of building resilient automation that adapts to asynchronous user interface updates without sacrificing test reliability.

---

## Future Improvements

- Validate multiple notification types.
- Expand support for warning and error notifications.
- Improve reusable notification helper functions.
- Generate structured notification validation reports.
- Integrate automated execution through GitHub Actions.

---


