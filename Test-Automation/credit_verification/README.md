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



## Full Implementation

The complete implementation of this project, including credit balance capture, document processing workflow validation, credit comparison, and result reporting, is available in:

➡️ [`credit_verification.py`](credit_verification.py)

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
