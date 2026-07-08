## Project Overview

Microsoft Narrator Compatibility demonstrates an automated approach to preparing a web application for manual screen reader testing using Microsoft Narrator. Developed with Python and Playwright, the project automates the environment setup by launching Narrator, connecting to an existing Chrome session, and attaching to the target application to provide a consistent starting point for accessibility evaluation.

By reducing repetitive manual setup, the automation allows testers to spend more time validating accessibility behavior while improving the consistency and efficiency of accessibility testing.

## Why I Built This

Preparing Microsoft Narrator for accessibility testing often involves repetitive setup before meaningful testing can begin. I developed this project to automate that preparation process, allowing testers to begin manual screen reader validation more quickly while maintaining a consistent testing environment across test sessions.

## Project Objectives

- Automate Microsoft Narrator startup.
- Connect Playwright to an existing Chrome debugging session.
- Attach to the target application automatically.
- Create a repeatable screen reader testing environment.
- Reduce repetitive accessibility test setup.
- 
## How It Works

The automation follows a structured workflow:

The automation performs the following workflow:

1. Launch Microsoft Narrator.
2. Connect to an existing Chrome instance using the Chrome DevTools Protocol (CDP).
3. Locate the target application tab.
4. Bring the application to the foreground.
5. Prepare a consistent environment for manual Narrator testing.
6. Allow the tester to perform screen reader validation using standard Narrator commands.

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
- Chrome DevTools Protocol (CDP)
  
## Skills Demonstrated

- Accessibility Testing
- Screen Reader Testing Support
- Playwright Automation
- Python Development
- Chrome DevTools Protocol (CDP)
- Test Environment Automation
- Windows Accessibility Tools
- Software Quality Assurance

## Challenges & Lessons Learned

Developing this project reinforced the importance of automating interactions with external accessibility tools while maintaining a reliable testing environment. It also highlighted the value of Chrome DevTools Protocol (CDP) for attaching Playwright to existing browser sessions, allowing accessibility testing to begin without launching a new browser instance.

## Future Improvements

Future enhancements may include:

- Add automated logging of test sessions.
- Expand support for additional screen reader workflows.
- Support automated browser startup and configuration.
- Improve diagnostic reporting.
- Explore integration with additional Windows accessibility tools.
