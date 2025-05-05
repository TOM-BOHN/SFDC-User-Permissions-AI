# Input Data Directory

This directory contains curated input tables and reference files used for analysis and processing in the Salesforce User Permissions AI project.

## Purpose
- **Staging Area:** Serves as the main staging area for cleaned, pre-processed, or reference data that is ready for further analysis, enrichment, or modeling.
- **Data Consistency:** Ensures that all downstream scripts and notebooks operate on a consistent, well-defined set of input data.

## Structure
- Files are typically in CSV or similar tabular formats, containing permission lists, user profiles, or other relevant metadata.
- Filenames should be descriptive and may include versioning or date information if appropriate.
- This directory may also include reference tables or mapping files used in the analysis pipeline.

## Input File Definitions

| Filename                                                       | Description                                                                                                  | Key Columns (if applicable)                |
|----------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|--------------------------------------------|
| user_permission_reference_data__full_list.csv                  | Master list of Salesforce user permissions, including names, API names, and descriptions.                    | Permission Name, API Name, Description     |
| user_permission_reference_data__sample.csv                     | Sample subset of Salesforce user permissions for testing and demonstration purposes.                         | Permission Name, API Name, Description     |
| user_permission_reference_data__sf_help_profile_perm_desc.csv  | Permissions and descriptions sourced from Salesforce Help's profile permission documentation.                | Permission Name, API Name, Description     |
| user_permission_reference_data__sf_ben_ten_high_risk_perms.csv | List of ten high-risk Salesforce permissions as identified by SalesforceBen, with names and API names.       | Permission Name, API Name                  |
| user_permission_reference_data__security_center_scope.csv      | Reference of permissions and their scope as defined in Salesforce Security Center documentation.             | Permission Name, API Name                  |

> For each new file, please add a row to this table with a brief description and key columns.

## Usage
- **Read-Write:** You may add or update files in this directory as new input data becomes available or as the project evolves.
- **Data Integrity:** When updating or replacing files, ensure that the new data is properly validated and documented.
- **Provenance:** Keep track of data sources and update this README or a data manifest with any significant changes.

## Adding or Updating Data
- Add new input files with clear, descriptive filenames.
- If replacing or updating an existing file, consider versioning or archiving the old file for traceability.
- Document the source and purpose of each file, either in this README or in a separate data manifest.

## References and Resources
- [Security Center Metrics](https://help.salesforce.com/s/articleView?id=xcloud.security_center_metrics_reference.htm&type=5)
- [User Profile Permission Descriptions](https://help.salesforce.com/s/articleView?id=000386319&type=1)
- [10 Crucial Salesforce Permissions You Should Not Assign to Users (SalesforceBen)](https://www.salesforceben.com/crucial-salesforce-permissions-you-should-not-assign-to-users/)

## For Contributors
- Ensure that any new or updated data is relevant, accurate, and well-documented.
- Coordinate with project maintainers before making large-scale changes or removing files.

## For Downstream Users
- Use the files in this directory as the primary input for analysis scripts, notebooks, or models.
- Do not edit files in place during analysis; instead, copy or export results to `data/output/` or another appropriate location.

---
**Note:** Maintaining clear documentation and provenance for input data is essential for reproducibility and collaboration in this project.