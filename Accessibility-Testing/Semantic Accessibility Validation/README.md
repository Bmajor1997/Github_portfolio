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
