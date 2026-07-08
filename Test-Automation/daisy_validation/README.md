## Project Overview

DAISY Validation demonstrates an automated approach to verifying accessible document conversion using Python and Playwright. The project performs an end-to-end document conversion workflow, downloads the generated DAISY package, validates the package structure, and compares the converted content against the original source document to verify conversion accuracy.

## Why I Built This

DAISY is a structured accessibility format used by individuals who rely on assistive technologies for reading digital content. Verifying a successful conversion requires more than confirming that the conversion completed—it also requires validating the generated package structure and ensuring the converted content accurately represents the source document.

## Project Objectives

- Validate end-to-end DAISY document conversion.
- Verify DAISY package generation.
- Confirm required DAISY package files are present.
- Validate downloaded package integrity.
- Compare converted content against the original document.
- Detect conversion failures through automated validation.

## How it Works

The automation performs the following workflow:

1. Upload a source PDF document.
2. Start the document conversion process.
3. Select DAISY as the target output format.
4. Complete the conversion workflow.
5. Download the generated DAISY ZIP package.
6. Validate the ZIP archive structure.
7. Verify required DAISY package files exist.
8. Compare the converted content against the original source document.
9. Report validation results.

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

The complete implementation includes automated document upload, DAISY format selection, conversion workflow automation, package validation, ZIP structure verification, content comparison, and Playwright-based end-to-end testing is available in:

➡️ [`daisy_validation`](test_daisy_validation.py)

## Technologies Used

- Python
- Playwright
- Pytest
- Pypdf
- ZIP File Validation
- DAISY
- Git
- GitHub

## Skills Demonstrated

- End-to-End Test Automation
- Accessibility Testing
- Accessible Document Validation
- Playwright Automation
- Python Development
- File Validation
- ZIP Package Inspection
- Content Comparison
- Regression Testing
- Software Quality Assurance

## Challenges and Lessons Learned

Developing this project reinforced the importance of validating generated output rather than simply confirming successful user interface interactions. The project demonstrated that accessibility-focused document conversion requires verifying package structure, required metadata, downloadable content, and text accuracy to ensure reliable output for assistive technology users.

## Future Improvements

- Perform deeper validation of DAISY package metadata.
- Validate additional DAISY specification requirements.
- Generate detailed HTML validation reports.
- Expand reusable validation helpers.
- Integrate automated execution through GitHub Actions.

