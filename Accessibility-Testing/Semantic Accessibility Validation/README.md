## Project Overview

Semantic Accessibility Validation demonstrates an automated approach to evaluating the semantic structure of a web application using Python and Playwright. The project focuses on identifying accessibility-related markup issues that may impact how assistive technologies interpret page content.

This project supports accessibility testing by checking whether key page elements use meaningful HTML structure, accessible roles, labels, and relationships that contribute to a more usable experience for assistive technology users.

## Why I Built This

Semantic HTML is an important foundation of accessible web applications. Even when a page appears visually correct, missing labels, unclear roles, or poor structural markup can create barriers for users relying on assistive technologies.

I developed this project to support accessibility testing by automating checks for semantic structure and identifying areas that may require further manual review.

## Project Objectives

- Evaluate semantic HTML structure.
- Identify accessibility-related markup issues.
- Validate accessible labels, roles, and element relationships.
- Support screen reader compatibility through structural testing.
- Create a repeatable workflow for semantic accessibility validation.

## How It Works

The automation follows a structured validation workflow:

1. Launch the target web application.
2. Inspect key page elements and accessibility-related attributes.
3. Validate semantic structure, roles, labels, and relationships.
4. Identify elements that may require accessibility review.
5. Report findings for follow-up validation.

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

➡️ [`test_semantic_accessibility_validation.py`](test_semantic_accessibility_validation.py)

## Technologies Used

- Python
- Playwright
- HTML
- ARIA
- Git
- GitHub

## Skills Demonstrated

- Accessibility Testing
- Semantic HTML Validation
- Playwright Automation
- Python Development
- ARIA Review
- Test Documentation
- Software Quality Assurance

## Challenges and Lessons Learned

Developing this project reinforced the importance of testing beyond visual behavior. Semantic accessibility requires evaluating how page structure, labels, roles, and relationships are exposed to assistive technologies.

This project strengthened my understanding of how automated validation can support accessibility review while still requiring thoughtful manual analysis for context-specific issues.

## Future Improvements

- Expand validation coverage across additional page templates.
- Add reporting for detected semantic accessibility issues.
- Integrate WCAG-related checks where appropriate.
- Improve reusable helper functions for semantic validation.
- Add GitHub Actions integration for automated execution.
