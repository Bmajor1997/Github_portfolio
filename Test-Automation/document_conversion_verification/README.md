## Project Overview

Document Upload Verification demonstrates an automated approach to validating a document upload workflow using Python and Playwright. The project verifies that a supported document can be selected, uploaded, and processed successfully through the application's upload interface.

This project supports quality assurance by creating a repeatable test for one of the most important user workflows in a document processing application.

## Why I Built This

Document Conversion is a critical workflow because users must be able to submit files before any processing or conversion can occur. Manual upload testing can become repetitive, especially when validating multiple supported file types.

I built this automation to reduce repetitive manual validation, confirm upload behavior consistently, and support regression testing for a core application feature.

## Project Objectives

- Validate successful document upload.
- Verify supported files can be selected through the upload input.
- Confirm the upload workflow progresses after submission.
- Identify upload or processing failures.
- Create a repeatable regression test for document upload behavior.

## Implementation Example

The following example demonstrates the core validation loop used to test document conversion across multiple output formats. 
The automation uploads the source document, waits for format selection, selects a target format, converts the file, attempts to download the result, 
and tracks passed or failed conversions.

```python
for target_format in OUTPUT_FORMATS:
    if target_format == current_format:
        continue

    reset_to_home(page)

    upload_document(page, file_path)
    click_start_and_select_format(page, file_name)
    wait_for_format_screen(page, file_name)

    selecting_format(page, target_format, current_format)
    click_convert(page)
    click_download_if_present(page, file_name, target_format)

    passed.append(f"{file_name} -> {target_format}")
```
## Full Implementation

The complete implementation of this project, including document upload, processing validation, output format selection, conversion, download handling, and pass/fail result tracking, is available in:

➡️ [`document_conversion_verification.py`](test_conversion_verification.py)

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
- File Upload Testing
- Workflow Validation
- Functional Testing
- Regression Testing
- Software Quality Assurance

## Challenges and Lessons Learned

Developing this project reinforced the importance of validating core user workflows with clear setup, reliable file handling, and repeatable automation. It also strengthened my understanding of how upload testing depends on stable test data, predictable file paths, and accurate validation of application state changes.

## Future Improvements

- Expand validation across additional supported file types.
- Add negative testing for unsupported files.
- Improve reusable upload helper functions.
- Add reporting for upload validation results.
- Integrate automated execution through GitHub Actions.
