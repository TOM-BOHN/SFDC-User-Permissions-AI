# Prompts Directory
This directory contains all LLM-related prompts and chains.

## Structure:
- templates/: Individual, reusable prompt templates
- chains/: Multi-step prompt orchestration
- system/: System-level prompts and configurations

## Best Practices:
1. Keep prompts modular and reusable
2. Version control your prompts
3. Document expected inputs/outputs
4. Include examples where helpful






----------------------------
# prompt_user_perm_category
----------------------------
## Worked Example (for illustration only – **omit** from real answers)
```
permission_name: "Modify All Data"
permission_description: "Grants the user the ability to read, create, edit, and delete **all** records in the org, ignoring sharing rules and field‑level security."

Expected JSON Output:
{{
  "risk_tier": "Mission Critical",
  "weighted_score": 4.8,
  "scores": {{
    "Data_Sensitivity": 5,
    "Scope_of_Impact": 5,
    "Configurational_Authority": 3,
    "External_Data_Exposure": 3,
    "Regulatory_Obligation": 5,
    "Segregation_of_Duties": 4,
    "Auditability": 3,
    "Reversibility": 4
  }},
  "rationale": "Permission overrides all sharing controls and touches sensitive data org‑wide. Misuse would violate multiple regulatory obligations and cannot be fully reversed without significant effort.",
  "confidence": "High"
}}
```



----------------------------
#prompt_user_perm_risk_rating
----------------------------

## Worked Example (for illustration only – **omit** from real answers)
```
permission_name: "Modify All Data"
permission_description: "Grants the user the ability to read, create, edit, and delete **all** records in the org, ignoring sharing rules and field‑level security."

Expected JSON Output:
{{
  "risk_tier": "Mission Critical",
  "weighted_score": 4.8,
  "scores": {{
    "Data_Sensitivity": 5,
    "Scope_of_Impact": 5,
    "Configurational_Authority": 3,
    "External_Data_Exposure": 3,
    "Regulatory_Obligation": 5,
    "Segregation_of_Duties": 4,
    "Auditability": 3,
    "Reversibility": 4
  }},
  "rationale": "Permission overrides all sharing controls and touches sensitive data org‑wide. Misuse would violate multiple regulatory obligations and cannot be fully reversed without significant effort.",
  "confidence": "High"
}}
```