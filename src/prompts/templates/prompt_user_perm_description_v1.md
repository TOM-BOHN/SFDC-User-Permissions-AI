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

Analyze the **Exapanded Description** against the **Evaluation Criteria**. Give step‑by‑step reasoning for your decision, citing the specific criteria that most influenced your rationale score.

# Evaluation Criteria

Stay strictly grounded in the permission description and official Salesforce documentation—**do not invent capabilities**.

- **Instruction Following** - The response demonstrates a clear understanding of the writing task instructions, satisfying all of the instruction's requirements.
- **Groundedness** - The response contains information consistent with the context of Salesforce User Permission. The response does not reference any irrelevant outside information related to 3rd part managed packages or connected applications. |
- **Specificity** - The response should contain specific details about the user permission and associated features and functionality. General information that applies to entire platform or a broad context should be avoided.
- **Conciseness** - The response provides relevant details without a significant loss in key information without being too verbose or terse.
- **Fluency** - The response is well-organized and easy to read.
- **Search Completeness** - The response provides high quality search results as references with sitations that come from the https://help.salesforce.com and https://salesforce.com domains.

# Evaluation Steps

- STEP 1 - **Search** - Search for and use results and citations within the https://help.salesforce.com and https://salesforce.com domains.
- STEP 2 -- **Related Feature** - Ensure the response identifies the specific **Salesforce Feature** and **Salesforce Cloud** related to the user permission.
- STEP 3 - **Exapanded Description** - Write an expanded description for the **User Permission** in paragraph form.
- STEP 4 – **Rational** -  Give step‑by‑step reasoning for your decision, citing the specific criteria that most influenced your rationale.
- STEP 5 - **Output** - Format the output exactly as specified in the JSON object described below—nothing else.

# Output Schema (JSON only)

```
{{
  "expanded_description": "<4‑10 succinct sentences describing the user permission in detail>",
  "salesforce_feature": "<Primary Salesforce Feature related to the user permission>",
  "salesforce_cloud": "<Primary Salesforce Cloud related to the user permission>",
  "rationale": "<3‑5 succinct sentences referencing the highest‑impact criteria for the quality score>",
  "confidence": "<High|Medium|Low>",
  "top_urls": ["<Primary or authoritative URLs related to the permission>"]
}}
```

# Input

- **Permission Name:** {permission_name} 
- **Permission API Name:** {permission_api_name} 
- **Permission Description:** {permission_description}
