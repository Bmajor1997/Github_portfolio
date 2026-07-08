## Project Overview

Credit Count Verification demonstrates an automated approach to locating and extracting the current credit balance displayed within a web application using Python and Playwright. The automation identifies credit-related text, extracts the numeric value using pattern matching, and verifies that a valid credit count is available for further testing.

## Why I Built This

Applications that rely on credit-based systems should clearly display available credits to users. Manually locating and confirming this information during testing can become repetitive, particularly during regression testing. I developed this project to automate credit count extraction and create a reusable foundation for future business rule validation.

## Project Objectives

- Retrieve the displayed credit count from the application.
- Extract credit values using flexible pattern matching.
- Support reliable credit detection across different page layouts.
- Verify that a valid credit value is available.
- Create a reusable foundation for future credit workflow validation.

## How it Works

The automation performs the following workflow:

1. Open the target web application.
2. Navigate to the page containing the credit balance.
3. Attempt to locate the credit value using a known selector, when available.
4. Fall back to scanning the visible page content.
5. Extract the numeric credit value using pattern matching.
6. Verify that a valid credit count was successfully retrieved.

## Implementation Example

The following example extracts the application's displayed credit balance using flexible pattern matching while supporting multiple text layouts and formatting styles.

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

The complete implementation includes credit value extraction, selector-based lookup, fallback text scanning, regular expression matching, and Playwright automation for retrieving displayed credit information.

➡️ [`credit_verification`](test_credits_verification.py)

## Technologies Used

- Python
- Playwright
- Pytest
- Git
- GitHub

## Skills Demonstrated

- Test Automation
- Playwright Automation
- Python Development
- Data Extraction
- Regular Expression (Regex) Pattern Matching
- Assertion Logic
- Dynamic Content Validation
- Software Quality Assurance

## Challenges and Lessons Learned

Developing this project reinforced the importance of building reliable data extraction logic for dynamic web applications. It also highlighted the value of combining selector-based retrieval with fallback text parsing to improve resilience when page layouts or UI elements change.

## Future Improvements

- Capture credit balances before and after document processing.
- Validate expected versus actual credit consumption.
- Add negative testing for insufficient credit scenarios.
- Expand support for additional credit-based workflows.
- Integrate automated execution through GitHub Actions.
