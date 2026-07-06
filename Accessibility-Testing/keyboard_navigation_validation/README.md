# Keyboard Navigation Validation

## Project Overview

Keyboard Navigation Validation demonstrates an automated approach to evaluating keyboard accessibility within a web application using Python and Playwright. The project validates keyboard-only navigation by verifying focus movement, detecting potential keyboard traps, and confirming that interactive elements remain accessible without requiring a mouse.

By automating these accessibility checks, the project reduces repetitive manual validation while providing a consistent and repeatable method for evaluating keyboard navigation behavior during software testing.

## Why I Built This

Keyboard accessibility is a fundamental component of accessible web applications, but manually validating navigation across multiple pages can be repetitive and time-consuming.

I developed this automation to streamline keyboard accessibility testing by creating a repeatable process for validating focus behavior, keyboard navigation, and potential accessibility issues during quality assurance testing.

## Project Objectives

- Validate keyboard-only navigation throughout a web application.
- Verify predictable focus movement between interactive elements.
- Detect potential keyboard traps.
- Reduce repetitive manual accessibility testing.
- Create a reusable automation workflow for keyboard accessibility validation.

## How It Works

The automation follows a structured workflow:

1. Launch the target web application.
2. Prepare the testing environment.
3. Navigate using keyboard input.
4. Track focus movement between interactive elements.
5. Validate expected keyboard behavior.
6. Detect potential keyboard accessibility issues.
7. Report test results.

## Technologies Used

- Python
- Playwright
- Git
- GitHub

## Skills Demonstrated

- Test Automation
- Accessibility Testing
- Playwright Automation
- Python Development
- Focus Management Validation
- Automation Debugging
- Software Quality Assurance

## Challenges and lessons learned 
Developing this automation reinforced the importance of synchronization, reliable focus detection, and building validation logic that behaves consistently 
across different execution environments. Debugging differences between local and remote execution also highlighted the need for maintainable automation and clear 
diagnostic logging.

## Future Improvements
- HTML reporting
- GitHub Actions integration
- Expanded keyboard interaction coverage
- Improved logging
- Reusable accessibility utilities
