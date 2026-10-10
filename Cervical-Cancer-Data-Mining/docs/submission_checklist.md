# Final Submission Checklist

## Project files

- [ ] Confirm the supplied UCI CSV is present at `data/raw/risk_factors_cervical_cancer.csv`.
- [ ] Keep the raw CSV unchanged; retain its provenance and cite the UCI dataset record.
- [ ] Include source scripts, `run_project.py`, and `requirements.txt`.
- [ ] Confirm `Practicals/` remains separate and unchanged.

## Report and figures

- [ ] Fill in the title-page student, roll number, college, department, semester, teacher, and submission-date fields in `docs/final_project_report.md`.
- [ ] Review the Markdown final report and PDF for readability, page breaks, image clarity, and accurate captions.
- [ ] Check all 16 referenced graph files and result tables are included in the submission folder or package.
- [ ] Include the project report draft only if the teacher requests development history; use the final report as the submission report.
- [ ] Ensure no missing personal details, college branding, or teacher approval are invented.

## Results and execution

- [ ] Retain the processed matrix and its provisional audit if permitted by the assignment’s data-sharing policy.
- [ ] Include K-Means iteration metrics, run summary, and assignments.
- [ ] Include DBSCAN parameter results and assignments.
- [ ] Include comparative metrics and per-cluster-size tables.
- [ ] Run `python run_project.py` in the intended submission environment and verify the exit status.
- [ ] Explain that rerunning regenerates processed data and derived outputs.
- [ ] Verify raw data hash before and after final execution if required by the teacher.

## Presentation and viva

- [ ] Rehearse the 6–7 minute sequence in `docs/demo_script.md`.
- [ ] Review the 36 questions in `docs/viva_questions.md` and adapt answers to the teacher’s rubric.
- [ ] Use `docs/presentation_outline.md` to prepare slides if a presentation is required.
- [ ] State that DBSCAN silhouette excludes noise and is not a direct full-record comparison to K-Means silhouette.
- [ ] Avoid calling clusters diagnoses or clinical risk groups.

## Decisions and teacher-specific requirements still pending

- [ ] Confirm the final project direction (clustering comparison versus the retained Biopsy-classification alternative).
- [ ] Confirm the nine clustering features and whether their measurement types are appropriate for Euclidean distance.
- [ ] Confirm median imputation, duplicate-copy removal, standardization, distance measure, and parameter ranges.
- [ ] Confirm whether the evaluation measures and comparison satisfy the course rubric.
- [ ] Confirm required cover page format, citation style, submission format, and any required demonstration length.
- [ ] Add personal/institutional details only after receiving them from the student or institution.

No teacher approval is claimed. The project is educational and is not a medical diagnostic tool.
