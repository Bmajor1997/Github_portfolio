## Project Overview

Credit Count Verification demonstrates an automated approach to extracting and validating the current credit balance displayed within a web application using Python and Playwright. The project reads the visible page content, identifies credit-related text patterns, and extracts the credit value for validation.

This project supports quality assurance by creating a repeatable way to verify that credit information is visible, readable, and available for future business rule validation.

## Why I Built This

Credit usage is an important business rule because users need accurate feedback about how many credits are available and how many are consumed during processing. Manual verification can be repetitive and prone to missed differences.

I built this automation to validate credit behavior consistently and support regression testing for credit-related workflows.

## Project Objectives

- Capture credit count before processing.
- Perform a document processing workflow.
- Capture credit count after processing.
- Compare expected and actual credit changes.
- Identify possible credit tracking issues.

## Implementation Example

The following example demonstrates the core credit extraction logic used to validate the application's displayed credit balance. The automation searches for credit-related text patterns, extracts the numeric value, and applies fallback matching to improve reliability across different page layouts.

```python
def extract_credits_best_effort(text: str) -> int | None:
    """
    Best-effort extraction:
    1) Prefer patterns near the word 'credit(s)'
    2) Fall back to a plausible standalone number (2-6 digits, allowing commas)
    """
    t = text or ""

    m = re.search(r"\b(\d{1,6}(?:,\d{3})*)\s*credits?\b", t, re.I)
    if not m:
        m = re.search(r"\bcredits?\s*(\d{1,6}(?:,\d{3})*)\b", t, re.I)

    if m:
        return int(m.group(1).replace(",", ""))

    m2 = re.search(r"\b\d{2,6}(?:,\d{3})*\b", t)
    if m2:
        return int(m2.group(0).replace(",", ""))

    return None
 ```   
## Full Implementation

The complete implementation of this project, including credit balance capture, document processing workflow validation, credit comparison, and result reporting, is available in:

➡️ [`credit_verification`](test_credit_verification.py)

## Technologies Used

- Python
- Playwright
- Pytest
- Git
- GitHub

## Skills Demonstrated

- Test Automation
- Business Rule Validation
- Playwright Automation
- Python Development
- Workflow Testing
- Assertion Logic
- Regression Testing
- Software Quality Assurance

## Challenges and Lessons Learned

Developing this project reinforced the importance of validating business logic in addition to user interface behavior. Credit tracking requires careful comparison of system state before and after a workflow, along with clear reporting when expected and actual values differ.

## Future Improvements

- Add support for multiple document types.
- Improve reporting for expected versus actual credit changes.
- Add negative testing for insufficient credits.
- Expand validation across additional credit-based workflows.
- Integrate automated execution through GitHub Actions.
