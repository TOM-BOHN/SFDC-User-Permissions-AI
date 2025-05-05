<!---
# Permission Category Evaluation Prompt Template  
# --------------------------------------------------
# This template can be imported and formatted with the specific
# `permission_name` and `permission_api_name` and `permission_description` variables to create
# a concrete evaluation prompt for any Salesforce permission.
# --------------------------------------------------
-->

# Instruction

You are a **Salesforce Certified Technical Architect (CTA)**.
Your task is to describe **Salesforce User Permissions** with an **Expanded Description**.
We will provide you with the permission name, api name, and a short permission description of what the Salesforce user permission (or capability) grants to a user.
Search the internet to find high quality references to use as sources in writing an Expanded Description.
Write a complete **Expanded Definition** for the following user permission and esure it aligns with the **Evaluation Criteria** for a high quality description.

- **Search** - Strictly search for and use results and citations within the https://help.salesforce.com and https://salesforce.com domains.
- **Exapanded Description** - Write an expanded description for the **User Permission** in paragraph form.
- **Related Feature** - Ensure the response identifies the specific **Salesforce Feature** and **Salesforce Cloud** related to the user permission.

Analyze the **Exapanded Description** against the **Evaluation Criteria**. Give step‑by‑step reasoning for your decision, citing the specific criteria that most influenced your quality score.

# Evaluation

## Metric Definition

- **Overall Quality Score** [aka weighted_score] measures how well the expanded description satisfies all the evaluation criteria as a measure of quality.
- **Criteria Quality Score** measure the how well the expanded description satisfies a specific criteria as a measure of quality.

## Evaluation Criteria 

For each criterion, assign an integer score from **1 (very low quality) to 5 (very high quality)**.
Stay strictly grounded in the permission description and official Salesforce documentation—**do not invent capabilities**.

## Criterion

| # | Criterion              | Weight | Definition                                                                                                                                                                                                                      |
|---|------------------------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | Instruction Following  | 0.30   | The response demonstrates a clear understanding of the writing task instructions, satisfying all of the instruction's requirements.                                                                                             |
| 2 | Groundedness           | 0.20   | The response contains information consistent with the context of Salesforce User Permission. The response does not reference any irrelevant outside information related to 3rd part managed packages or connected applications. |
| 3 | Specificity            | 0.20   | The response should contain specific details about the user permission and associated features and functionality. General information that applies to entire platform or a broad context should be avoided.                     |
| 4 | Conciseness            | 0.10   | The response provides relevant details without a significant loss in key information without being too verbose or terse.                                                                                                        |
| 5 | Fluency                | 0.10   | The response is well-organized and easy to read.                                                                                                                                                                                | 
| 6 | Search Completeness    | 0.10   | The response provides high quality search results as references with sitations that come from the https://help.salesforce.com and https://salesforce.com domains.                                                               |

## Match Scoring Scale

| Weighted Score Range | Score | Quality Label          | Description                           | Percentage Quality |
|----------------------|--------------------------------|---------------------------------------|--------------------|
| 4.5 – <5.0           | 5     | **Perfect Quality**    | Perfect or 100% quality; spot on.     | 100%               |
| 3.5 – <4.5           | 4     | **High Quality**       | Strong or 75% quality; pretty close.  |  75%               |
| 2.5 – <3.5           | 3     | **Moderate Quality**   | Fair or 50% quality; decent fit.      |  50%               |
| 1.5 – <2.5           | 2     | **Low Quality**        | Partial or 25% quality; some overlap. |  25%               |
| 1.0 – <1.5           | 1     | **No Quality**         | None or 0% quality; totally off.      |   0%               |

# Evaluation Steps

- STEP 1 - **Search** - Strictly search for and use results and citations within the https://help.salesforce.com and https://salesforce.com domains.
- STEP 2 -- **Related Feature** - Ensure the response identifies the specific **Salesforce Feature** and **Salesforce Cloud** related to the user permission.
- STEP 3 - **Exapanded Description** - Write an expanded description for the **User Permission** in paragraph form.
- STEP 4 - **Score Criterion** - Evaluate the **Exapanded Description** against each criterion to obtain a **criterion quality score** (1-5), noting specific factors.
- STEP 5 - **Score Overall** - Each criterion quality score is **multiplied** by its weight and **sumed** to obtain the **overall quality score (weighted_score)** (round to one decimal place).  
- STEP 6 - **Quality Rating** - Select the best fitting **Quality Label** using the match score scale.
- STEP 7 – **Summarize** - Aggregate quality findings. 
- STEP 8 - **Output** - Format the output exactly as specified in the JSON object described below—nothing else.


# Output Schema (JSON only)

```
{{
  "expanded_description": "<4‑10 succinct sentences describing the user permission in detail>",
  "salesforce_feature": "<Primary Salesforce Feature related to the user permission>",
  "salesforce_cloud": "<Primary Salesforce Cloud related to the user permission>",
  "quality_score_label": "<No Quality|Low Quality|Moderate Quality|High Quality|Perfect Quality>",
  "quality_score_value": "<1|2|3|4|5>",
  "weighted_quality_score": <float>,
  "scores": {{
    "Instruction_Following": <int>,
    "Groundedness": <int>,
    "Specificity": <int>,
    "Conciseness": <int>,
    "Fluency": <int>,
    "Search_Completeness": <int>
  }},
  "rationale": "<3‑5 succinct sentences referencing the highest‑impact criteria for the quality score>",
  "confidence": "<High|Medium|Low>",
  "top_urls": ["<Primary or authoritative URLs related to the permission>"]
}}
```

# Input

- **Permission Name:** {permission_name} 
- **Permission API Name:** {permission_api_name} 
- **Permission Description:** {permission_description}
