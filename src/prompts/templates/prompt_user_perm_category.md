# Permission Category Evaluation Prompt Template  
# --------------------------------------------------
# This template can be imported and formatted with the specific
# `permission_name` and `permission_api_name` and `permission_description` variables to create
# a concrete evaluation prompt for any Salesforce permission.
# --------------------------------------------------

# Instruction
You are a **Salesforce security risk assessor**.
Your task is to categorize user security permission int **permission categories**.
We will provide you with the permission name and a short description of what the Salesforce user permission (or capability) grants to a user.
Analyze the permission against the **Evaluation Criteria** below and assign one of the twenty **Permission Categories** defined based on similarity of the category and the permission.
Give step‑by‑step reasoning for your decision, citing the specific criteria that most influenced your categorization.

# Evaluation

## Metric Definition
**Permission Match Score** [aka weighted_score] measures the overall simiarity and quality of the match between the category and the permission.
**Criteria Match Score** measure the simiarity and quality of the match between the permission and the category for a specific criteria.


## Evaluation Criteria  
For each criterion, assign an integer score from **1 (very low match) to 5 (very high match)**.
Stay strictly grounded in the permission description and official Salesforce documentation—**do not invent capabilities**.


## Criterion
| # | Criterion                                 | Weight| Why it separates these 20 domains                                                                                                                                         |
|-----------------------------------------------|-------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | Primary Product or Feature Anchor         | 0.20   | Distinct product family or feature set that anchors a category. The permission should explicitly mention objects, components, or APIs that live in that product area.    |
| 2 | Administrative vs End-User Function       | 0.20   | Categories split along who wields the power: org-/setup-level admins vs feature operators.                                                                               |  
| 3 | Data Interaction Pattern                  | 0.20   | Whether the permission changes metadata, data records, analytics datasets, or external streams helps identify Data-centric domains                                       |
| 4 | Platform Layer or Add-On Alignment        | 0.20   | Some domains correspond to premium add-ons. A permission that only exists when that managed package or license is present belongs to that domain.                        | 
| 5 | Intended User Persona or Business Process | 0.20   | Several categories map to clear personas or verticals. If the permission description references those workflows, boost that category.                                    |

## Match Scoring Scale
5 – **Exact Match**: Perfect or 100% match; spot on.  
4 – **High Match**: Strong or 75% match; pretty close.
3 – **Moderate Match**: Fair or 50% match; decent fit.
2 – **Low Match**: Partial or 25% match; some overlap.
1 – **No Match**: None or 0% match; totally off.


# Salesforce Permission Categories
- **General Admin**: Focus on broad system administration, organization configuration, and user setup tasks. This category often includes permissions for mass record operations (e.g., transferring records, managing billing), customizing the application, and deploying changes between Salesforce environments. Improper use can significantly affect the entire org's functionality and security.
- **Security Admin**: Primarily concerned with safeguarding the Salesforce org, controlling authentication methods, and securing access points. Typical examples include managing IP restrictions, password policies, and multi-factor authentication (MFA) to ensure user login integrity and data protection. Misuse can compromise the org's overall security posture.
- **User Management**: Govern the creation, management, and oversight of user access within the org. Permissions in this category let admins manage profiles, permission sets, roles, and external users, as well as reset passwords and unlock user accounts. Unauthorized use can result in improper access or privilege escalation.
- **Data Admin**: Provide the ability to view or modify data across the entire Salesforce org. These are among the most powerful permissions, letting users see or change all organizational data—often restricted to a highly trusted set of individuals because any misuse can have a broad operational or compliance impact.
- **Import and Export**: Encompass bringing data into Salesforce or extracting it externally. Common examples include importing leads, exporting report data, or scheduling routine data exports. Mistakes or misuse can compromise data integrity or lead to large-scale data leakage.
- **Agentforce and Einstein**: Covers Salesforce's AI-driven features, including Einstein (e.g., Einstein Assistant, Einstein Search, Einstein Bots) and any Agentforce automation. These permissions allow users to train AI models, manage predictions, or deploy AI-driven features. Misuse can result in inaccurate recommendations, exposure of sensitive data via automated insights, or disruption of key AI processes.
- **Report and Dashboard**: Allow users to create, customize, manage, or schedule reports and dashboards that display organizational data. This category ranges from basic report-building to advanced features like dynamic dashboards, snapshot management, and controlling report folder access. Improper assignment can expose sensitive analytics or disrupt key organizational metrics.
- **Developer**: Enable more technical users to create, modify, and manage custom programmatic functionality (e.g., Apex code, APIs, Flows, or Metadata). These are typically high-risk since they can override normal security and automate core business processes, requiring strict oversight to prevent vulnerabilities or data corruption.
- **User Interface**: Control how users experience Salesforce, from toggling between Classic and Lightning to customizing sidebars or controlling interface elements. While often lower in direct data risk, some UI permissions (like mass emailing or custom in-app guidance) can still affect adoption, user workflows, or inadvertently reveal data.
- **Object**: Focus on the creation, editing, and viewing of specific Salesforce objects (e.g., Accounts, Contacts, Contracts, Leads, and custom objects). They also include actions like activating contracts, editing read-only fields, or viewing encrypted data—all of which can carry compliance implications if misused.
- **Shield and Event Monitoring**: Encompass Salesforce Shield features like Platform Encryption, Event Monitoring, and Transaction Security. These permissions allow administrators to encrypt data, track user actions, and set security policies based on events. Misuse can result in non-compliance, incomplete logging, or exposure of sensitive logs.
- **Chatter and Communities**: Manage collaboration features and external community access. Tasks include moderating Chatter posts, creating or managing Experience Cloud sites, inviting external members, and controlling file or feed content. These can be high impact if external access is misconfigured or if sensitive chatter feeds are exposed.
- **Data Cloud**: Relevant to Salesforce Data Cloud (also referred to as Customer 360 or Data Cloud/CDP). Permissions here revolve around connecting the org to Data Cloud, accessing Data Cloud explorers and data sets, or managing large-scale customer data for analytics and personalization. Misuse can lead to massive privacy and compliance risks.
- **CRM Analytics**: Also known as Wave or Tableau CRM. Let users build, explore, and share advanced analytics beyond standard reports/dashboards, often using Einstein Discovery or dataflows. Improper usage could expose broader data sets or produce inaccurate analytics that mislead decision-makers.
- **Slack and Quip**: Involve Slack integrations (e.g., managing user mappings, Slack app connections, Slack Elevate) and Quip features (e.g., creating collaborative documents, accessing Quip metrics). Misconfiguration can lead to unauthorized data sharing or insufficient collaboration controls, exposing internal chat content or sensitive documents.
- **Commerce**: Pertinent to orgs running Salesforce B2B or B2C Commerce and Order Management. Permissions can include managing orders, fulfillment, return processes, repricing, or registering guest buyers. Because these involve financial transactions and customer data, improper assignment can severely impact revenue, logistics, or compliance.
- **Field Service**: Apply to Salesforce Field Service (FSL) functionality, covering scheduling, appointment lifecycle, dispatch console, and mobile settings. These permissions control on-site service operations, resource skills, and territory planning. Misuse can disrupt field operations or expose customer service data.
- **Marketing Cloud and Pardot**: Address Marketing Cloud (Email Studio, Journey Builder, Mobile Studio) or Pardot (Account Engagement) use cases. These permissions include creating journeys, managing subscriber data, and launching campaigns. Misuse can result in large-scale unauthorized messaging, exposure of contact data, or brand damage.
- **CPQ**: Focus on Salesforce CPQ (Configure, Price, Quote) features, including product configuration, pricing rules, advanced approvals, and discount schedules. Any misconfiguration can lead to financial losses, incorrect quoting, or compliance issues with pricing disclosures.
- **Industry Cloud**: Apply to specialized Salesforce Industry Clouds (e.g., Health Cloud, Financial Services Cloud, Manufacturing Cloud). Permissions here manage industry-specific objects, compliance settings, and specialized workflows. Misuse could breach industry regulations (e.g., HIPAA in Health Cloud) or compromise sensitive financial records. 


## Salesforce Permission Categories Table

| Permission Category Name     | Type          | Order |
|------------------------------|---------------|-------|
| General Admin                | Core Platform | 1     |
| Security Admin               | Core Platform | 2     |
| User Management              | Core Platform | 3     |
| Data Admin                   | Core Platform | 4     |
| Import and Export            | Core Platform | 5     |
| Agentforce and Einstein      | Core Platform | 6     |
| Report and Dashboard         | Core Platform | 7     |
| Developer                    | Core Platform | 8     |
| User Interface               | Core Platform | 9     |
| Object                       | Core Platform | 10    |
| Shield and Event Monitoring  | Cloud         | 11    |
| Chatter and Communities      | Cloud         | 12    |
| Data Cloud                   | Cloud         | 13    |
| CRM Analytics                | Cloud         | 14    |
| Slack and Quip               | Cloud         | 15    |
| Commerce                     | Cloud         | 16    |
| Field Service                | Cloud         | 17    |
| Marketing Cloud and Pardot   | Cloud         | 18    |
| CPQ                          | Cloud         | 19    |
| Industry Cloud               | Cloud         | 20    | 


# Evaluation Steps
STEP 1 - **Score Criterion** - Evaluate the permission against each criterion to obtain a **criterion match score** (1-5), noting specific matching factors.
STEP 2 - **Score Permission** - Each criterion match score is **multiplied** by its weight and **sumed** to obtain the **permission match score (weighted_score)** (round to one decimal place).  
STEP 3 - **Match Rating** - Select the best fitting category using the highest permission match ratting to assign the **Maping** to a category.
STEP 4 – **Summarize** - Aggregate findings and assess your confidence in the assigned category.  
STEP 5 - **Output** - Format the output exactly as specified in the JSON object described below—nothing else.


# Output Schema (JSON only)
```
{{
  "permission_category_label": "<General Admin|Security Admin|User Management|Data Admin|Import and Export|Agentforce and Einstein|Report and Dashboard|Developer|User Interface|Object|Shield and Event Monitoring|Chatter and Communities|Data Cloud|CRM Analytics|Slack and Quip|Commerce|Field Service|Marketing Cloud and Pardot|CPQ|Industry Cloud>",
  "permission_category_order": "<1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20>",
  "match_rating_tier": "<No Match|Low Match|Moderate Match|High Match|Exact Match>",
  "match_rating_score": "<1|2|3|4|5>",
  "weighted_match_score": <float>,
  "scores": {{
    "Data_Sensitivity": <int>,
    "Scope_of_Impact": <int>,
    "Configurational_Authority": <int>,
    "External_Data_Exposure": <int>,
    "Regulatory_Obligation": <int>,
    "Segregation_of_Duties": <int>,
    "Auditability": <int>,
    "Reversibility": <int>
  }},
  "rationale": "<3‑5 succinct sentences referencing the highest‑impact criteria for the match>",
  "confidence": "<High|Medium|Low>"
}}
```

# Input
**Permission Name:** {permission_name} 
**API Name:** {permission_api_name} 
**Permission Description:** {permission_description}
