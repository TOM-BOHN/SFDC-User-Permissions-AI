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
Your task is to categorize user security permission into **Permission Categories**.
We will provide you with the permission name and a short description of what the Salesforce user permission (or capability) grants to a user.
Analyze the permission against the **Evaluation Criteria** below and assign one of the twenty **Permission Categories** defined based on similarity of the category and the permission.
Give step‑by‑step reasoning for your decision, citing the specific criteria that most influenced your categorization.

# Evaluation

## Metric Definition

- **Permission Match Score** [aka weighted_score] measures the overall simiarity and quality of the match between the category and the permission.
- **Criteria Match Score** measure the simiarity and quality of the match between the permission and the category for a specific criteria.


## Evaluation Criteria 

For each criterion, assign an integer score from **1 (very low match) to 5 (very high match)**.
Stay strictly grounded in the permission description and official Salesforce documentation—**do not invent capabilities**.


## Criterion

| # | Criterion                                 | Weight | Why it separates these 20 domains                                                                                                                                        |
|---|-------------------------------------------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | Primary Product or Feature Anchor         | 0.20   | Distinct product family or feature set that anchors a category. The permission should explicitly mention objects, components, or APIs that live in that product area.    |
| 2 | Administrative vs End-User Function       | 0.20   | Categories split along who wields the power: org-/setup-level admins vs feature operators.                                                                               |  
| 3 | Data Interaction Pattern                  | 0.20   | Whether the permission changes metadata, data records, analytics datasets, or external streams helps identify Data-centric domains                                       |
| 4 | Platform Layer or Add-On Alignment        | 0.20   | Some domains correspond to premium add-ons. A permission that only exists when that managed package or license is present belongs to that domain.                        | 
| 5 | Intended User Persona or Business Process | 0.20   | Several categories map to clear personas or verticals. If the permission description references those workflows, boost that category.                                    |

## Match Scoring Scale

| Weighted Score Range | Score | Match Label          | Description                         | Percentage Match |
|----------------------|------------------------------|-------------------------------------|------------------|
| 4.5 – <5.0           | 5     | **Exact Match**      | Perfect or 100% match; spot on.     | 100%             |
| 3.5 – <4.5           | 4     | **High Match**       | Strong or 75% match; pretty close.  |  75%             |
| 2.5 – <3.5           | 3     | **Moderate Match**   | Fair or 50% match; decent fit.      |  50%             |
| 1.5 – <2.5           | 2     | **Low Match**        | Partial or 25% match; some overlap. |  25%             |
| 1.0 – <1.5           | 1     | **No Match**         | None or 0% match; totally off.      |   0%             |

# Salesforce Permission Categories

- **General Admin**: [1] [Core Platform] Focuses on organization-wide settings that establish the foundational operational parameters and identity of the Salesforce instance. Permissions typically include managing company profile information (e.g., name, address), fiscal year settings, currency management, default locale/language/time zones, license management and tracking, monitoring overall system/storage usage, managing org-wide email deliverability settings, basic sandbox lifecycle management (creation/refresh only), and potentially managing the organization's billing and contract details with Salesforce. This category explicitly excludes permissions related to user setup/access control, security policy configuration, data model/interface customization, data access/manipulation, and application deployment, which are governed by other specific categories.
- **Security Admin**: [2] [Core Platform] Focuses on securing the Salesforce organization by controlling authentication, access policies, and monitoring security posture. Permissions typically cover managing password policies, multi-factor authentication (MFA) setup, IP restrictions, session settings, login flows, Health Check configuration, managing Connected Apps for API client authorization and access, and potentially managing certificates and keys used for authentication or integration security.
- **User Management Admin**: [3] [Core Platform] Governs the complete lifecycle and access configuration for all users (internal, external site/portal users, identity users). Permissions encompass creating and managing users; defining and assigning all forms of access control (including profiles, permission sets, permission set groups, roles, public groups, queues); delegating specific administrative tasks to users; managing password policies, resets, and session settings; unlocking accounts; and overseeing user login access and activation/deactivation. This category holds the primary responsibility for defining who can access Salesforce and what foundational permissions they are granted through profiles and permission sets.
- **Data Admin**: [4] [Core Platform] Provides extensive rights to view, modify, and manage data across the entire Salesforce organization, often bypassing standard record ownership and sharing rules. Core permissions include "View All Data" and "Modify All Data". This category also explicitly governs permissions for performing org-wide mass data operations (such as Mass Transfer Records, Mass Delete Records, potentially Mass Update Addresses), managing data storage utilization (monitoring, identifying candidates for archiving/deletion), and configuring tools related to data quality, duplicate management, or data governance rules across the org.
- **Import and Export**: [5] [Core Platform] Encompasses permissions required to bring data into Salesforce or extract data out of it using standard platform tools and services designed for bulk data handling by end-users or administrators. Common examples include using the Data Import Wizard, Data Loader client application (or its API under user context), setting up standard Data Exports ('Weekly Data Export'), and the 'Export Reports' permission. This category is distinct from building custom API integrations (Developer) or possessing org-wide data modification rights (Data Admin).
- **Agentforce**: [6] [Core Platform] Focuses specifically on permissions for building, deploying, managing, and interacting with Salesforce's autonomous AI agents (Agentforce). This includes using Agent Builder, defining agent capabilities via topics and actions (linking Flows, Apex, Prompt Templates, APIs), setting operational guardrails, managing pre-built agents (e.g., Service Agent, Sales Agent, Campaign Optimizer), and granting users the ability to trigger or utilize these agents. It encompasses the framework for AI that can independently reason, plan, and execute tasks based on data or triggers.   
- **Einstein and AI**: [7] [Core Platform] Governs permissions related to the broader Salesforce AI platform (Einstein), including foundational predictive and generative capabilities integrated across the CRM. This covers enabling and managing features like Einstein Search, Einstein Activity Capture, Einstein Prediction Builder, utilizing cloud-specific AI insights (e.g., Sales Cloud Einstein scoring, Service Cloud Einstein classification recommendations), accessing AI within CRM Analytics (Einstein Discovery), and configuring core generative AI settings or the Einstein Trust Layer.
- **Report and Dashboard**: [8] [Core Platform] Allows users to create, customize, manage, view, subscribe to, or schedule reports and dashboards for data visualization and analysis. Permissions range from basic report running and building to managing report/dashboard folders, creating custom report types, configuring dynamic dashboards, managing reporting snapshots, and potentially accessing more advanced analytics features if not covered under CRM Analytics.
- **Developer**: [9] [Core Platform] Enables the creation, modification, testing, and deployment of custom functionality, automation, integrations, and data structures within Salesforce. Permissions cover both declarative configuration impacting the org's structure and automation (creating/modifying custom objects, fields, relationships, validation rules, complex Flows) and programmatic development (Apex classes/triggers, Lightning Web Components, Visualforce pages, platform events, APIs). This includes developing customizations and automation for specific clouds, packages, or features (e.g., writing a trigger for CPQ objects or a Flow for Health Cloud), although package-specific administrative settings and configuration permissions belong to their respective categories. This category also includes managing metadata, administering sandboxes for development/testing, configuring and executing automated tests, and owning the deployment process for moving configuration and code between environments (e.g., using Change Sets, Salesforce CLI, DevOps Center, or other deployment tools).
- **User Interface**: [10] [Core Platform] Controls the configuration and customization of the Salesforce user interface to optimize user experience, navigation, and workflow efficiency across devices. Permissions include managing page layout assignments, configuring Lightning record pages (components, visibility rules), customizing application navigation (apps, tabs, utility bars), controlling standard/custom object list views (creation, sharing, visibility), managing compact layouts, configuring search layouts and global search settings, and potentially managing themes/branding or deploying in-app guidance and user engagement features. This category focuses on how users visually interact with Salesforce records and navigate the application using the standard interface.
- **Object Access**: [11] [Core Platform] Focuses on the ability to create, read, edit, and delete specific standard or custom object records (e.g., Accounts, Contacts, Opportunities, Cases, custom objects). It also includes permissions for specific actions related to objects, such as activating contracts, editing fields marked as read-only on page layouts (if granted via permission), converting leads, or viewing potentially encrypted field data (requires separate decryption permission usually).
- **Data Cloud**: [12] [Core Platform Add-Ons] Relates specifically to Salesforce Data Cloud (formerly Customer Data Platform/CDP). Permissions govern connecting data sources to Data Cloud, configuring data streams, managing data mapping and harmonization, creating calculated insights, building segments, managing activation targets, and accessing Data Cloud features like explorers and data sets.
- **CRM Analytics**: [13] [Core Platform Add-Ons] Pertains to CRM Analytics (formerly Tableau CRM / Einstein Analytics / Wave). Permissions allow users to upload data, build complex dataflows/recipes, create and manage datasets, build advanced dashboards (lenses and apps), explore data interactively, and potentially use Einstein Discovery for AI-driven insights within the analytics platform.
- **Chatter and Communities**: [14] [Core Platform Add-Ons] Manages internal collaboration via Chatter and external access via Experience Cloud (formerly Communities). Permissions include moderating Chatter feeds/files, creating/managing Experience Cloud sites, managing Experience Cloud users (partners, customers), configuring site access/security, inviting external members, and controlling content sharing within feeds or sites.
- **Shield and Event Monitoring**: [15] [Core Platform Add-Ons] Encompasses permissions related to Salesforce Shield components: Platform Encryption, Event Monitoring, and Transaction Security. Permissions allow administrators to manage encryption keys, select fields for encryption, access and analyze detailed event log files (tracking user actions, API calls, performance), set up real-time event-based security policies (Transaction Security), and manage Field Audit Trail. Salesforce Shield's Event Monitoring provides granular visibility into user activities, data access, and changes, enabling proactive security measures and compliance verification.
- **UNKNOWN**: [99] [Other] Includes any permission that has no clear mapping to any of the established permission categories in the table. 


## Salesforce Permission Categories Table

| Permission Category Name         | Type                  | Order |
|----------------------------------|-----------------------|-------|
| General Admin                    | Core Platform         | 1     |
| Security Admin                   | Core Platform         | 2     |
| User Management Admin            | Core Platform         | 3     |
| Data Admin                       | Core Platform         | 4     |
| Import and Export                | Core Platform         | 5     |
| Agentforce                       | Core Platform         | 6     |
| Einstein and AI                  | Core Platform         | 7     |
| Report and Dashboard             | Core Platform         | 8     |
| Developer                        | Core Platform         | 9     |
| User Interface                   | Core Platform         | 10    |
| Object Access                    | Core Platform         | 11    |
| Data Cloud                       | Core Platform Add-Ons | 12    |
| CRM Analytics                    | Core Platform Add-Ons | 13    |
| Chatter and Communities          | Core Platform Add-Ons | 14    |
| Shield and Event Monitoring      | Core Platform Add-Ons | 15    |
| UNKNOWN                          | Other                 | 99    |


# Evaluation Steps

- STEP 1 - **Score Criterion** - Evaluate the permission against each criterion to obtain a **criterion match score** (1-5), noting specific matching factors.
- STEP 2 - **Score Overall Match** - Each criterion match score is **multiplied** by its weight and **sumed** to obtain the **category match score (weighted_score)** (round to one decimal place).  
- STEP 3 - **Match Rating** - Select the best fitting **Permission Category** using the highest **category match score** to assign the **Permission Category** to each **User Permission**.
- STEP 4 – **Summarize** - Aggregate findings and assess your confidence in the assigned **Permission Category** mapping.  
- STEP 5 - **Output** - Format the output exactly as specified in the JSON object described below—nothing else.


# Output Schema (JSON only)

```
{{
  "permission_category_label": "<General Admin|Security Admin|User Management Admin|Data Admin|Import and Export|Agentforce|Einstein and AI|Report and Dashboard|Developer|User Interface|Object Access|Data Cloud|CRM Analytics|Chatter and Communities|Shield and Event Monitoring|UNKNOWN>",
  "permission_category_order": "<1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|99>",
  "match_rating_tier": "<No Match|Low Match|Moderate Match|High Match|Exact Match>",
  "match_rating_score": "<1|2|3|4|5>",
  "weighted_match_score": <float>,
  "scores": {{
    "Primary_Product_or_Feature_Anchor": <int>,
    "Administrative_vs_End_User_Function": <int>,
    "Data_Interaction_Pattern": <int>,
    "Platform_Layer_or_Add_On_Alignment": <int>,
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
