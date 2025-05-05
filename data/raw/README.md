# Raw Data Directory

This directory contains the original, unprocessed data files scraped from Salesforce websites and other relevant sources. These files serve as the primary input for all downstream data processing, extraction, and analysis tasks in this project.

## Purpose
- **Source of Truth:** The files in this folder represent the canonical source data for Salesforce user permissions and related metadata.
- **Reproducibility:** Keeping the raw data intact ensures that all processing steps can be reproduced and audited from the original source.

## Structure
- Files are typically in HTML, MHTML, or other web archive formats, as directly downloaded or scraped.
- Filenames may encode metadata such as permission set type, Salesforce org ID, or scrape date.
- No manual edits or transformations should be performed on these files.

## Usage
- **Read-Only:** Do not modify, delete, or overwrite files in this directory. All data cleaning, transformation, and analysis should be performed on copies or outputs in other directories (e.g., `data/input/`, `data/output/`).
- **Adding Data:** If new raw data is scraped, add it here with a descriptive filename and update any relevant documentation or data manifests.
- **Provenance:** Always retain the original file to ensure traceability and reproducibility of results.

## For Contributors
- Treat this directory as append-only. If you need to update or correct data, add a new file and document the change in the project changelog or data manifest.
- If you discover corrupted or irrelevant files, consult with the project maintainers before removal.

## For Downstream Users
- Use the files in this directory as input for data extraction scripts, but never edit them directly.
- Refer to the `data/input/` and `data/output/` directories for processed and cleaned data ready for analysis.

---
**Note:** Maintaining the integrity of the raw data is critical for the transparency and reproducibility of this project.
