## Project Overview

Keyboard Navigation Validation demonstrates an automated approach to evaluating keyboard accessibility within a web application using Python and Playwright. The project validates keyboard-only navigation by verifying focus movement, reverse navigation, dropdown keyboard interaction, and detecting potential keyboard traps throughout an end-to-end user workflow.

## Why I Built This

Although manual keyboard testing remains essential, automating common navigation patterns helps identify accessibility issues more efficiently and provides repeatable regression testing.

## Project Objectives

- Validate keyboard-only navigation throughout a web application.
- Verify predictable focus movement using Tab and Shift+Tab.
- Detect potential keyboard traps.
- Validate keyboard interaction within dropdown menus.
- Support accessibility regression testing through repeatable automation.
- Reduce repetitive manual keyboard accessibility testing.

## How It Works

The automation follows a structured workflow:

1. Launch the target web application.
2. Prepare the testing environment.
3. Validate forward keyboard navigation using Tab.
4. Validate reverse navigation using Shift+Tab.
5. Detect potential keyboard traps.
6. Verify keyboard interaction within dropdown controls.
7. Complete an end-to-end document conversion workflow using only keyboard interactions.
8. Report detected accessibility issues.

## Implementation Example

The following function demonstrates how the automation validates keyboard navigation by tracking focus movement after each Tab key press. It flags possible accessibility issues when focus does not move or repeats unexpectedly.

```python
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
```
The complete implementation is available here:

➡️ [test_keyboard_navigation_validation.py](test_keyboard_navigation_validation.py)

## Technologies Used

- Python
- Playwright
- Pytest
- Git
- GitHub

## Skills Demonstrated

- Accessibility Testing
- Keyboard Accessibility Validation
- Focus Management
- Playwright Automation
- Python Test Development
- End-to-End Test Automation
- Custom Validation Logic
- Software Quality Assurance

## Challenges and lessons learned 
Developing this automation reinforced the importance of synchronization, reliable focus detection, and accurately tracking keyboard navigation across dynamic web interfaces. Debugging differences between local and remote execution also highlighted the importance of maintainable automation, reusable helper functions, and clear diagnostic logging.

## Future Improvements
- HTML reporting
- GitHub Actions integration
- Expanded keyboard interaction coverage
- Improved logging
- Reusable accessibility utilities
- Expand validation to additional keyboard interactions such as Escape, Enter, and Space key behavior.
