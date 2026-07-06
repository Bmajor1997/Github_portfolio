# Microsoft Narrator Compatibility

## Project Overview

Microsoft Narrator Compatibility demonstrates an automated approach to preparing a web application for accessibility testing with Microsoft Narrator, the built-in Windows screen reader. Developed using Python and Playwright, the project automates the setup process required to establish a consistent testing environment for evaluating screen reader interactions and keyboard accessibility.

By reducing repetitive manual setup, the automation allows testers to spend more time validating accessibility behavior while improving the consistency and efficiency of accessibility testing.

## Why I Built This

Preparing Microsoft Narrator for accessibility testing often requires repetitive setup before meaningful testing can begin. I developed this project to automate that preparation process, creating a repeatable workflow that allows accessibility testing to begin more quickly and consistently.

The project demonstrates how automation can support accessibility testing by reducing manual effort while maintaining a reliable testing environment.

## Project Objectives

- Automate the setup process for Microsoft Narrator.
- Create a repeatable accessibility testing workflow.
- Reduce repetitive manual configuration.
- Improve consistency during screen reader testing.
- Support efficient accessibility validation.

## How It Works

The automation follows a structured workflow:

1. Launch the target web application.
2. Prepare the testing environment.
3. Start Microsoft Narrator.
4. Configure the environment for screen reader testing.
5. Establish a consistent starting point for accessibility validation.
6. Complete setup for manual or automated accessibility testing.

## Implementation Example

The following function demonstrates how the script connects to an existing Chrome session through CDP, searches open browser tabs, and attaches to the target application for Narrator accessibility testing.

```python
def open_existing_example_page(playwright):
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

            if "example.com" in current_url:
                page.bring_to_front()
                print(f"Attached to existing application tab: {page.url}")
                return browser, chrome_context, page
        except Exception:
            continue

    raise Exception("No existing target application tab was found in the open Chrome window.")
```
The complete implementation is available here:
➡️ [`microsoft_narrator_compatibility.py`](microsoft_narrator_compatibility.py)
## Technologies Used

- Python
- Playwright
- Microsoft Narrator
- Windows Accessibility Tools

## Skills Demonstrated

- Accessibility Testing
- Screen Reader Validation
- Playwright Automation
- Python Development
- Test Environment Preparation
- Automation Workflow Design
- Software Quality Assurance

## Challenges & Lessons Learned

Developing this project reinforced the importance of creating reliable automation around external accessibility tools. It highlighted the need for consistent timing, repeatable environment preparation, and maintainable automation that supports accessibility testing without introducing unnecessary complexity.

The project also strengthened my understanding of integrating assistive technologies into automated QA workflows.

## Future Improvements

Future enhancements may include:

- Additional Narrator validation scenarios.
- Expanded compatibility testing.
- Improved logging and reporting.
- Integration with GitHub Actions.
- Support for additional accessibility workflows.
