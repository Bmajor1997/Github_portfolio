## Project Overview

DAISY Validation demonstrates an automated approach to verifying accessible document output using Python and Playwright. The project validates that a DAISY output can be generated successfully and supports quality review by checking whether the conversion workflow reaches the expected result.

This project supports quality assurance by creating a repeatable validation process for an accessibility-focused document format.

## Why I Built This

DAISY is an accessible document format used to support structured reading experiences. Validating DAISY output requires more than confirming that a conversion button was clicked; the workflow must confirm that the output is generated and available for review.

I built this automation to reduce repetitive manual validation and support consistent testing of DAISY conversion behavior.

## Project Objectives

- Validate successful DAISY output generation.
- Verify that DAISY can be selected as an output format.
- Confirm the conversion workflow completes.
- Identify failures during DAISY processing.
- Create a repeatable workflow for accessible document output testing.

The following example demonstrates the core DAISY output validation logic. After the DAISY ZIP file is downloaded, the automation verifies that the output is a valid ZIP archive, checks for required DAISY package files, confirms files are not empty, and compares source document text against the generated DAISY content.

```python
def validate_daisy_zip(zip_path, source_file):
    if not zipfile.is_zipfile(zip_path):
        return {"status": "FAIL", "reason": "Not a valid ZIP file"}

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        file_list = zip_ref.namelist()

    if not file_list:
        return {"status": "FAIL", "reason": "ZIP is empty"}

    has_opf = any(file.endswith(".opf") for file in file_list)
    has_ncx = any(file.endswith(".ncx") for file in file_list)

    if not has_opf:
        return {"status": "FAIL", "reason": "ZIP file missing: .opf"}

    if not has_ncx:
        return {"status": "FAIL", "reason": "ZIP file missing: .ncx"}

    non_empty_file_count = 0

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for file in file_list:
            if zip_ref.getinfo(file).file_size > 0:
                non_empty_file_count += 1

    if non_empty_file_count == 0:
        return {
            "status": "FAIL",
            "reason": "Every file in the DAISY package equals 0 bytes."
        }

    source_text = extract_pdf_text(source_file)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        package_text = ""
        for file in file_list:
            if Path(file).suffix.lower() in {".opf", ".ncx", ".html", ".xhtml", ".xml", ".smil"}:
                package_text += zip_ref.read(file).decode("utf-8", errors="ignore").lower()

    daisy_text = normalize_text(package_text)

    if source_text[:200] not in daisy_text:
        return {
            "status": "FAIL",
            "reason": "Expected source document text was not found in the DAISY output"
        }

    return {"status": "PASS", "files": file_list}
```

## Full Implementation

The complete implementation of this project, including DAISY format selection, conversion workflow validation, output verification, and result reporting, is available in:

➡️ [`daisy_validation.py`](daisy_validation.py)

## Technologies Used

- Python
- Playwright
- Pytest
- DAISY
- Git
- GitHub

## Skills Demonstrated

- Test Automation
- Playwright Automation
- Python Development
- Accessible Document Validation
- Workflow Testing
- Output Format Validation
- Regression Testing
- Software Quality Assurance

## Challenges and Lessons Learned

Developing this project reinforced the importance of validating accessibility-focused output formats beyond simple UI interaction. DAISY validation requires confirming that the workflow progresses correctly, the output format is selectable, and the conversion result is available for review.

This project strengthened my understanding of how automation can support specialized QA validation for accessible document delivery.

## Future Improvements

- Add deeper validation of DAISY output structure.
- Verify expected DAISY package files.
- Add reporting for conversion success and failure states.
- Improve reusable helper functions for output validation.
- Integrate automated execution through GitHub Actions.

