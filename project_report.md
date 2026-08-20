---

# 9. PROJECT_REPORT.md

Create `PROJECT_REPORT.md`:

```markdown
# Project Report: Skill Gap Analyzer

## 1. Introduction

The Skill Gap Analyzer is a Python command-line application developed
for Project #58 of the Learn Depth Track 1 Level-4 Python Project
Challenge Library.

The application compares a candidate's current skills with the
requirements of a selected role. It identifies matched skills,
missing skills, priority gaps, and an overall skill-match percentage.

## 2. Problem Understanding

Candidates often know their current skills but may not know which
skills are most important for a target role. A simple list comparison
is not sufficient because role skills have different levels of
importance.

The application therefore needs to normalize user input, compare
skills, classify missing skills, calculate a meaningful score, and
produce a clear report.

## 3. Requirements Analysis

The system must:

- Accept candidate details and skills
- Support multiple target roles
- Compare candidate and role skills
- Identify matched and missing skills
- Prioritize missing skills
- Calculate a match percentage
- Validate incorrect or empty input
- Search and filter information
- Save analysis history
- Generate readable reports
- Handle file and JSON errors
- Include meaningful automated tests

## 4. Proposed Approach

The application uses a modular architecture. Role requirements are
stored in JSON. User-entered skills are normalized before comparison.
Set membership is used for efficient skill matching.

Skills are divided into three role categories:

- Required
- Important
- Optional

These categories determine priority and scoring weight.

## 5. System Design

The program follows this flow:

1. Load role data
2. Display the main menu
3. Accept candidate information
4. Validate and normalize skills
5. Select a target role
6. Compare candidate skills with role requirements
7. Calculate the weighted match percentage
8. Generate the skill-gap report
9. Save the analysis
10. Optionally export a text report

## 6. Project Architecture

- `main.py` controls the CLI and menu.
- `models.py` defines the domain objects.
- `validator.py` validates and normalizes input.
- `analyzer.py` contains comparison and priority logic.
- `data_manager.py` handles JSON persistence.
- `report_generator.py` formats and exports reports.
- `test_analyzer.py` contains automated tests.

## 7. Implementation

Candidate skills are split using commas, semicolons, pipes, or new
lines. Every skill is stripped, converted to lowercase, and checked
against an alias dictionary.

Examples:

- `PYTHON` becomes `python`
- `ML` becomes `machine learning`
- `sklearn` becomes `scikit-learn`
- `OOP` becomes `object-oriented programming`

The normalized candidate skills are compared with normalized role
skills.

## 8. Important Technical Decisions

### Modular Design

Responsibilities are separated into individual files. This improves
readability, testing, and maintainability.

### Object-Oriented Programming

Dataclasses represent:

- Candidate
- Role
- SkillGap
- SkillGapReport

OOP is used where the problem naturally contains structured entities.

### JSON Storage

JSON was selected because it is free, human-readable, lightweight,
and appropriate for a local application.

### Weighted Scoring

Core required skills have a greater effect on the result than optional
skills.

Weights are:

- Required: 3
- Important: 2
- Optional: 1

### Safe File Writing

History is written to a temporary file before replacing the original
history file. This reduces the risk of leaving partially written JSON.

## 9. Data Structures Used

### Lists

Lists store ordered skills, reports, and search results.

### Dictionaries

Dictionaries store role information, category rules, aliases, and
priority ordering.

### Sets

Sets support efficient skill membership checking and identification
of additional skills.

### Objects

Objects group related data and behavior into clear domain models.

## 10. Validation

The application validates:

- Empty candidate names
- Empty skill lists
- Excessively long names
- Duplicate skills
- Invalid role selections
- Invalid priority filters
- Invalid sorting options
- Invalid role data

## 11. Exception Handling

The program handles:

- `FileNotFoundError`
- `json.JSONDecodeError`
- `OSError`
- `ValueError`
- Custom `ValidationError`
- Custom `DataManagerError`
- Keyboard interruption

Broad, silent `except` blocks are avoided.

## 12. Persistence

Role definitions are loaded from `data/roles.json`.

Completed analyses are appended to
`data/analysis_history.json`.

Reports may also be exported as text files in the `reports` directory.

## 13. Testing

Ten automated tests were created using `unittest`.

The tests cover:

- Complete matches
- Partial matches
- Empty input
- Duplicate values
- Aliases
- Capitalization
- Unknown roles
- Priority filtering
- Role searching
- History persistence

Manual testing was also performed through the CLI.

## 14. Challenges Encountered

### Inconsistent Skill Names

Users may enter different names for the same skill.

Solution: A normalization and alias system was implemented.

### Meaningful Priority

Treating every missing skill equally would make the report less useful.

Solution: Skills are assigned High, Medium, or Low priority according
to their role category.

### Reliable Persistence

Missing or corrupted files could cause the application to crash.

Solution: File operations use targeted exception handling and clear
error messages.

## 15. Limitations

- The application uses locally maintained role information.
- It does not automatically read resumes.
- It does not use live job-market information.
- It uses normalized exact matching rather than semantic matching.
- Priorities depend on manually classified role requirements.

## 16. Future Scope

Future versions could include:

- Resume upload
- Job-description upload
- NLP-based skill extraction
- Semantic skill matching
- Learning-roadmap generation
- Course recommendations
- Custom role management
- Web interface
- Live job-market integration

## 17. Conclusion

The Skill Gap Analyzer satisfies the project requirement by comparing
candidate skills against role requirements and prioritizing missing
skills. It demonstrates Python fundamentals, modular programming,
object-oriented design, collections, validation, exception handling,
searching, filtering, sorting, testing, file handling, and JSON
persistence.

The final result is a functional and explainable Python application
that can be extended in future versions.
```
