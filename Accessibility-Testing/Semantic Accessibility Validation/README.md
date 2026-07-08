## Project Overview

Semantic Accessibility Validation demonstrates an automated approach to validating the accessibility structure of a web application using Python, Playwright, and axe-core. It combines automated accessibility scanning with custom validation logic to inspect headings, landmarks, graphic labels, and user-facing error messages that influence how assistive technologies interpret page content.

## Why I Built This

Semantic HTML is an important foundation of accessible web applications. Even when a page appears visually correct, missing labels, unclear roles, or poor structural markup can create barriers for users relying on assistive technologies.

I developed this project to support accessibility testing by automating checks for semantic structure and identifying areas that may require further manual review.

## Project Objectives

- Validate page accessibility using axe-core.
- Verify semantic HTML structure.
- Inspect heading hierarchy.
- Validate landmark regions.
- Verify accessible graphic labels.
- Review user-facing error messages.
- Support repeatable accessibility regression testing.

## How It Works

The automation follows a structured validation workflow:

1. Launch the target web application.
2. Run axe-core accessibility analysis.
3. Validate graphic labels and ARIA relationships.
4. Verify heading hierarchy and document structure.
5. Inspect required page landmarks.
6. Review visible error messages for accessibility and clarity.
7. Report any detected accessibility violations.

## Implementation Example

The following function demonstrates custom semantic accessibility validation by inspecting visible heading elements, checking for empty headings, verifying that an `h1` exists, and detecting skipped heading levels.

```python
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
```
## Full Implementation

The complete implementation of this project, including semantic structure checks, accessibility-related attribute validation, and Playwright-based inspection logic, is available in:

➡️ [`test_semantic_accessibility.py`](test_semantic_accessibility.py)

## Technologies Used

- Python
- Playwright
- pytest
- axe-core
- HTML
- ARIA
- Git
- GitHub
 
## Skills Demonstrated

- Accessibility Testing
- Automated Accessibility Validation
- Semantic HTML Review
- Playwright Automation
- Python Test Development
- ARIA Validation
- Test Automation
- Quality Assurance
- Custom Validation Logic

## Challenges and Lessons Learned

Developing this project reinforced the importance of testing beyond visual behavior. Semantic accessibility requires evaluating how page structure, labels, roles, and relationships are exposed to assistive technologies.

This project strengthened my understanding of how automated validation can support accessibility review while still requiring thoughtful manual analysis for context-specific issues.

## Future Improvements

- Expand validation coverage across additional page templates.
- Reporting for detected semantic accessibility issues.
- Integrate WCAG-related checks where appropriate.
- Improve reusable helper functions for semantic validation.
- GitHub Actions integration for automated execution.
- Automated accessibility reports for CI/CD pipelines.
