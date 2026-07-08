
## Project Overview

Remediation Checkpoints demonstrates an automated approach to validating accessibility remediation results throughout an end-to-end document conversion workflow using Python and Playwright. The project verifies document processing, evaluates accessibility-related checkpoints, compares source and converted content, and validates structural accessibility features including headings, tables, links, OCR quality, AI-generated image descriptions, and document integrity.

## Why I Built This

Accessibility remediation involves much more than determining whether a document successfully converts. Quality assurance also requires validating document structure, accessibility metadata, OCR quality, content preservation, page counts, and other remediation checkpoints. I developed this project to automate these validations and provide a repeatable framework for reviewing remediation accuracy across multiple document types.

## Project Objectives

- Validate end-to-end accessibility remediation workflows.
- Verify document processing and conversion results.
- Compare source and converted document content.
- Evaluate accessibility-related remediation checkpoints.
- Detect structural accessibility issues.
- Validate AI-generated image descriptions.
- Verify page counts, tables, headings, lists, and hyperlinks.
- Support repeatable accessibility regression testing.

## How it Works 

1. Upload a source document.
2. Complete the document conversion workflow.
3. Download the converted document.
4. Validate page count and preview behavior.
5. Compare source and converted text quality.
6. Verify AI-generated image descriptions.
7. Compare headings, lists, and tables.
8. Validate PDF table tagging.
9. Verify hyperlink preservation.
10. Report remediation checkpoint results.

The following example demonstrates the checkpoint-based validation workflow used after document conversion. Each checkpoint records accessibility-related quality indicators, including page count verification, preview validation, AI-generated image descriptions, OCR quality, heading preservation, table validation, hyperlink preservation, and overall remediation accuracy.

```python
result = {
    "source": str(source_path),
    "converted": None,
    "ui_page_count": None,
    "preview_pages_visible": None,
    "pages_converted_ok": None,
    "ai_desc_ok": None,
    "ocr_quality": None,
    "headings": None,
    "lists": None,
    "tables": None,
    "table_tagging": None,
    "links": None,
    "error": None,
}

chosen_label, converted_path = run_flow_and_download(
    page,
    source_path,
    DOWNLOADS_DIR
)

result["ui_page_count"] = page_count_from_ui_any_scope(page)
result["preview_pages_visible"] = preview_pages_visible_count_any_scope(page)
result["ai_desc_ok"] = count_ai_markers_in_text(
    extract_text_from_file(converted_path)
)
result["ocr_quality"] = compare_ocr_quality_best_effort(
    source_path,
    converted_path
)
result["headings"] = compare_documents(
    normalize_all_headings(extract_all_headings(file_path=source_path)),
    normalize_all_headings(extract_all_headings(file_path=converted_path))
)
```

## Full Implementation

The complete implementation includes document conversion automation, remediation checkpoint validation, accessibility comparison, OCR quality evaluation, document structure analysis, hyperlink validation, table tagging verification, and detailed workflow reporting. is available in:

➡️ [`remediation_checkpoints`](test_remediation_accuracy_checkpoints.py)

## Technologies Used

- Python
- Playwright
- pytest
- BeautifulSoup
- pypdf
- pandas
- openpyxl
- python-docx
- python-pptx
- odfpy
- Git
- GitHub

## Skills Demonstrated

- End-to-End Test Automation
- Accessibility Validation
- Document Conversion Testing
- Playwright Automation
- Python Development
- OCR Quality Analysis
- Document Structure Validation
- PDF Accessibility Testing
- Content Comparison
- Hyperlink Validation
- Table Tagging Validation
- Multi-Format Document Parsing
- Software Quality Assurance

## Challenges and Lessons Learned

Developing this project reinforced the importance of validating accessibility remediation beyond simple conversion success. Effective remediation testing requires comparing document structure, page counts, text quality, accessibility metadata, tables, links, and AI-generated descriptions to ensure converted documents preserve both content and accessibility features.

## Future Improvements

- Expand validation across additional document formats.
- Generate HTML or JSON remediation reports.
- Add configurable validation thresholds.
- Improve comparison reporting for structural differences.
- Support batch remediation validation.
- Integrate automated execution through GitHub Actions.
