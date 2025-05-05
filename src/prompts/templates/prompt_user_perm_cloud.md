<!---
# Permission Category Evaluation Prompt Template  
# --------------------------------------------------
# This template can be imported and formatted with the specific
# `permission_name` and `permission_api_name` and `permission_description` variables to create
# a concrete evaluation prompt for any Salesforce permission.
# --------------------------------------------------
-->

# Instruction

You are a **Salesforce security risk assessor**.
Your task is to categorize user security permission into **Salesforce Clouds**.
We will provide you with the permission name and a short description of what the Salesforce user permission (or capability) grants to a user.
Analyze the permission against the **Evaluation Criteria** below and assign one of the **Salesforce Clouds** defined based on similarity of the Salesforce Cloud and the User Permission.
Give step‑by‑step reasoning for your decision, citing the specific criteria that most influenced your cloud selection.

# Evaluation

## Metric Definition

- **Cloud Match Score** [aka weighted_score] measures the overall simiarity and quality of the match between the Salesforce Cloud and the User Permission.
- **Criteria Match Score** measure the simiarity and quality of the match between Salesforce Cloud and the User Permission for a specific criteria.


## Evaluation Criteria 

For each criterion, assign an integer score from **1 (very low match) to 5 (very high match)**.
Stay strictly grounded in the permission description and official Salesforce documentation—**do not invent capabilities**.


## Criterion

| # | Criterion                                 | Weight | Why it separates these domains                                                                                                                                           |
|---|-------------------------------------------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | Primary Product or Feature Anchor         | 0.50   | Distinct product family or feature set that anchors a cloud. The permission should explicitly mention objects, components, or APIs that live in that product area.       |
| 2 | Core Cloud or Add-On Alignment            | 0.25   | Some domains correspond to premium add-ons. A permission that only exists when that managed package or license is present belongs to that domain.                        | 
| 3 | Intended User Persona or Business Process | 0.25   | Several categories map to clear personas or verticals. If the permission description references those workflows, boost that category for cloud alignment.                |

## Match Scoring Scale

| Weighted Score Range | Score | Match Label          | Description                         | Percentage Match |
|----------------------|------------------------------|-------------------------------------|------------------|
| 4.5 – <5.0           | 5     | **Exact Match**      | Perfect or 100% match; spot on.     | 100%             |
| 3.5 – <4.5           | 4     | **High Match**       | Strong or 75% match; pretty close.  |  75%             |
| 2.5 – <3.5           | 3     | **Moderate Match**   | Fair or 50% match; decent fit.      |  50%             |
| 1.5 – <2.5           | 2     | **Low Match**        | Partial or 25% match; some overlap. |  25%             |
| 1.0 – <1.5           | 1     | **No Match**         | None or 0% match; totally off.      |   0%             |


# Salesforce Clouds

- **Sales Cloud**: [1] [Cloud] Includes permissions specific to Sales Cloud features designed to manage the entire sales process. This covers managing leads and conversion processes, opportunity management (stages, products, quotes), account and contact management for sales purposes, sales forecasting (quotas, adjustments), territory management, managing sales teams, using Sales Console, and potentially features like Sales Engagement (Cadences) or basic Quoting (if CPQ isn't used).
- **Service Cloud**: [2] [Cloud] Contains permissions specific to Service Cloud features focused on customer service and support across multiple channels. This includes case management (creation, assignment rules, escalation), managing support channels (Email-to-Case, Web-to-Case, Chat, Messaging, Phone integration via CTI), knowledge base management (Salesforce Knowledge), entitlement management and milestones (SLAs), using the Service Console, and potentially AI-driven features like Service Cloud Einstein (case classification, recommendations) or basic Field Service features if the full FSL package isn't used.
- **Marking Cloud and Pardot**: [3] [Cloud] Address Marketing Cloud (Email Studio, Journey Builder, Mobile Studio) or Pardot (Account Engagement) use cases. These permissions include creating journeys, managing subscriber data, and launching campaigns. Misuse can result in large-scale unauthorized messaging, exposure of contact data, or brand damage.
- **Commerce Cloud**: [4] [Cloud] Pertains to permissions for Salesforce B2B and B2C Commerce platforms, as well as Order Management. This includes managing storefront setup (Experience Builder for D2C), catalogs and products, pricing (price books, entitlements), promotions, managing carts and checkouts, processing orders, managing fulfillment and inventory, handling returns/RMAs, and potentially managing guest buyer profiles or B2B buyer accounts.
- **Slack and Quip**: [5] [Cloud] Involves permissions for integrating Salesforce with Slack and using Quip collaboration features. For Slack, this includes managing Slack app connections, user mappings, configuring features like Sales Cloud for Slack or Service Cloud for Slack, potentially managing Slack Elevate integrations. For Quip, it covers creating/managing collaborative documents, embedding Quip docs in Salesforce records, managing Quip user access, and accessing Quip metrics.
- **CPQ**: [6] [Cloud Add-Ons] Focuses on permissions related to Salesforce CPQ (Configure, Price, Quote) functionality, designed for complex product configuration and quoting processes. Permissions include managing products and price books specific to CPQ, configuring product bundles and rules (configuration, validation, pricing, alert rules), setting up discount schedules and approvals, generating quote documents, and managing contracts and renewals originating from CPQ quotes. Salesforce CPQ helps automate quoting, ensuring accuracy for complex sales.
- **Field Service**: [7] [Cloud Add-Ons] Applies to permissions for Salesforce Field Service (FSL) functionality, used to manage mobile workforce operations. Permissions cover managing service territories and resources (technicians), defining skills and availability, scheduling and dispatching service appointments (using the Dispatch Console or automation), managing work orders and service lifecycles, configuring the FSL mobile app settings, tracking inventory used in the field, and analyzing field service performance. FSL extends Service Cloud for managing on-site customer service.
- **Financial Services Cloud**: [8] [Industries] Includes permissions specific to Financial Services Cloud (FSC), tailored for banking, wealth management, and insurance industries. Permissions cover managing financial accounts, client and household relationship mapping (using the relationship map and groups), tracking financial goals and life events, managing insurance policies or claims, utilizing interaction summaries, potentially configuring compliance features (e.g., related to KYC or suitability), and accessing FSC-specific analytics.
- **Healthcare & Life Sciences Cloud**: [9] [Industries] Encompasses permissions for both Health Cloud (focused on providers, payers, patients) and Life Sciences Cloud (focused on pharma, biotech, medical device companies). For Health Cloud: managing patient data (often integrating with EHRs), care coordination tools, patient timelines, care plans, utilization management, provider network management. For Life Sciences: managing clinical trials, provider relationship management, advanced therapy management, sales programs for medical devices, regulatory compliance tracking. Both emphasize adherence to healthcare regulations.
- **Consumer Goods Cloud**: [10] [Industries] Contains permissions specific to Consumer Goods (CG) Cloud, designed for companies managing retail execution and B2B relationships in the consumer goods sector. Permissions include managing store visits, planning routes, executing in-store tasks (audits, surveys, inventory checks, planogram compliance), managing promotions and trade funds (Trade Promotion Management - TPM), handling orders specific to retail channels, account planning, and using the CG Cloud offline mobile app.
- **Communications Cloud**: [11] [Industries] Includes permissions for Communications Cloud, tailored for telecommunications and media companies. Permissions relate to managing the Enterprise Product Catalog (EPC) for complex product/service offerings, using Industries CPQ for accurate quoting of telco/media bundles, Industries Order Management (OM) for decomposing and fulfilling complex orders across systems, managing subscriber lifecycles, handling billing accounts, potentially using Digital Commerce for B2B/B2C self-service, and managing contracts.
- **Manufacturing Cloud**: [12] [Industries] Contains permissions specific to Manufacturing Cloud, aimed at connecting sales, service, and operations for manufacturers. Permissions cover managing Sales Agreements (long-term volume/price contracts), Account-Based Forecasting (combining sales forecasts with operational plans), managing partner relationships (distributors, suppliers) via Experience Cloud for Manufacturing, tracking inventory, potentially managing warranties or service parts, and utilizing manufacturing-specific analytics.
- **Nonprofit Cloud**: [13] [Industries] Includes permissions for Nonprofit Cloud, designed to meet the specific needs of nonprofit organizations. Permissions cover Fundraising features (managing donations, grants, recurring giving, payment processing), Program Management (tracking programs, services delivered, client participation), Case Management (for managing client needs and services), Outcome Management (measuring impact and mission success), potentially volunteer management, and managing marketing/engagement specific to donors and constituents.
- **General Industries Clouds**: [14] [Industries] Acts as a general category for permissions that might apply to Salesforce Industry Clouds not listed a separatecategories (such as Energy & Utilities, Public Sector). Permissions here typically involve managing industry-specific features, standard or custom objects, configuring specialized workflows or automation tailored to industry processes, managing compliance settings relevant to the sector, and utilizing industry-specific console apps or analytics.
- **Core Platform**: [15] [Core Platform] Acts as a general category for permissions that all apply to the core platform and control general features and functionality used across the clouds and industries.
- **Data Cloud**: [16] [Core Platform Add-Ons] Relates specifically to Salesforce Data Cloud (formerly Customer Data Platform/CDP). Permissions govern connecting data sources to Data Cloud, configuring data streams, managing data mapping and harmonization, creating calculated insights, building segments, managing activation targets, and accessing Data Cloud features like explorers and data sets.
- **CRM Analytics**: [17] [Core Platform Add-Ons] Pertains to CRM Analytics (formerly Tableau CRM / Einstein Analytics / Wave). Permissions allow users to upload data, build complex dataflows/recipes, create and manage datasets, build advanced dashboards (lenses and apps), explore data interactively, and potentially use Einstein Discovery for AI-driven insights within the analytics platform.
- **Chatter and Communities**: [18] [Core Platform Add-Ons] Manages internal collaboration via Chatter and external access via Experience Cloud (formerly Communities). Permissions include moderating Chatter feeds/files, creating/managing Experience Cloud sites, managing Experience Cloud users (partners, customers), configuring site access/security, inviting external members, and controlling content sharing within feeds or sites.
- **Shield and Event Monitoring**: [19] [Core Platform Add-Ons] Encompasses permissions related to Salesforce Shield components: Platform Encryption, Event Monitoring, and Transaction Security. Permissions allow administrators to manage encryption keys, select fields for encryption, access and analyze detailed event log files (tracking user actions, API calls, performance), set up real-time event-based security policies (Transaction Security), and manage Field Audit Trail. Salesforce Shield's Event Monitoring provides granular visibility into user activities, data access, and changes, enabling proactive security measures and compliance verification.
- **UNKNOWN**: [99] [Other] Includes any permission that has no clear mapping to any of the established Salesforce Clouds in the table. 


## Salesforce Permission Categories Table

| Salesforce Cloud                 | Type                  | Order |
|----------------------------------|-----------------------|-------|
| Sales Cloud                      | Cloud                 |  1    |
| Service Cloud                    | Cloud                 |  2    |
| Marking Cloud and Pardot         | Cloud                 |  3    |
| Commerce Cloud                   | Cloud                 |  4    |
| Slack and Quip                   | Cloud                 |  5    |
| CPQ                              | Cloud Add-Ons         |  6    |
| Field Service                    | Cloud Add-Ons         |  7    |
| Financial Services Cloud         | Industries            |  8    |
| Healthcare & Life Sciences Cloud | Industries            |  9    |
| Consumer Goods Cloud             | Industries            | 10    |
| Communications Cloud             | Industries            | 11    |
| Manufacturing Cloud              | Industries            | 12    |
| Nonprofit Cloud                  | Industries            | 13    |
| General Industries Cloud         | Industries            | 14    |
| Core Platform                    | Core Platform         | 15    |
| Data Cloud                       | Core Platform Add-Ons | 16    |
| CRM Analytics                    | Core Platform Add-Ons | 17    |
| Chatter and Communities          | Core Platform Add-Ons | 18    |
| Shield and Event Monitoring      | Core Platform Add-Ons | 19    |
| UNKNOWN                          | Other                 | 99    |


# Evaluation Steps

- STEP 1 - **Score Criterion** - Evaluate the permission against each criterion to obtain a **criterion match score** (1-5), noting specific matching factors.
- STEP 2 - **Score Overall Match** - Each criterion match score is **multiplied** by its weight and **sumed** to obtain the **cloud match score (weighted_score)** (round to one decimal place).  
- STEP 3 - **Match Rating** - Select the best fitting **Salesforce Cloud** using the highest **cloud match score** to assign the **Slaersforce Cloud** to each **User Permission**.
- STEP 4 – **Summarize** - Aggregate findings and assess your confidence in the assigned **Slaersforce Cloud** mapping.  
- STEP 5 - **Output** - Format the output exactly as specified in the JSON object described below—nothing else.


# Output Schema (JSON only)

```
{{
  "permission_cloud_label": "<Sales Cloud|Service Cloud|Marking Cloud and Pardot|Commerce Cloud|Slack and Quip|CPQ|Field Service|Financial Services Cloud|Healthcare & Life Sciences Cloud|Consumer Goods Cloud|Communications Cloud|Manufacturing Cloud|Nonprofit Cloud|General Industries Cloud|Core Platform|Data Cloud|CRM Analytics|Chatter and Communities|Shield and Event Monitoring|UNKNOWN>",
  "permission_cloud_order": "<1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|99>",
  "match_rating_tier": "<No Match|Low Match|Moderate Match|High Match|Exact Match>",
  "match_rating_score": "<1|2|3|4|5>",
  "weighted_match_score": <float>,
  "scores": {{
    "Primary_Product_or_Feature_Anchor": <int>,
    "Core_Cloud_or_Add_On_Alignment ": <int>,
    "Intended_User_Persona_or_Business_Process": <int>
  }},
  "rationale": "<3‑5 succinct sentences referencing the highest‑impact criteria for the match>",
  "confidence": "<High|Medium|Low>"
}}
```

# Input

- **Permission Name:** {permission_name} 
- **Permission API Name:** {permission_api_name} 
- **Permission Description:** {permission_description}
- **Permission Expanded Description:** {permission_expanded_description}