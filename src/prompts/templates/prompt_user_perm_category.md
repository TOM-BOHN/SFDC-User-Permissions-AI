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
- **Shield and Event Monitoring**: [15] [Add-On to Cloud] Encompasses permissions related to Salesforce Shield components: Platform Encryption, Event Monitoring, and Transaction Security. Permissions allow administrators to manage encryption keys, select fields for encryption, access and analyze detailed event log files (tracking user actions, API calls, performance), set up real-time event-based security policies (Transaction Security), and manage Field Audit Trail. Salesforce Shield's Event Monitoring provides granular visibility into user activities, data access, and changes, enabling proactive security measures and compliance verification.
- **Sales Cloud**: [16] [Cloud] Includes permissions specific to Sales Cloud features designed to manage the entire sales process. This covers managing leads and conversion processes, opportunity management (stages, products, quotes), account and contact management for sales purposes, sales forecasting (quotas, adjustments), territory management, managing sales teams, using Sales Console, and potentially features like Sales Engagement (Cadences) or basic Quoting (if CPQ isn't used).
- **Service Cloud**: [17] [Cloud] Contains permissions specific to Service Cloud features focused on customer service and support across multiple channels. This includes case management (creation, assignment rules, escalation), managing support channels (Email-to-Case, Web-to-Case, Chat, Messaging, Phone integration via CTI), knowledge base management (Salesforce Knowledge), entitlement management and milestones (SLAs), using the Service Console, and potentially AI-driven features like Service Cloud Einstein (case classification, recommendations) or basic Field Service features if the full FSL package isn't used.
- **Marking Cloud and Pardot**: [18] [Cloud] Address Marketing Cloud (Email Studio, Journey Builder, Mobile Studio) or Pardot (Account Engagement) use cases. These permissions include creating journeys, managing subscriber data, and launching campaigns. Misuse can result in large-scale unauthorized messaging, exposure of contact data, or brand damage.
- **Commerce Cloud**: [19] [Cloud] Pertains to permissions for Salesforce B2B and B2C Commerce platforms, as well as Order Management. This includes managing storefront setup (Experience Builder for D2C), catalogs and products, pricing (price books, entitlements), promotions, managing carts and checkouts, processing orders, managing fulfillment and inventory, handling returns/RMAs, and potentially managing guest buyer profiles or B2B buyer accounts.
- **Slack and Quip**: [20] [Cloud] Involves permissions for integrating Salesforce with Slack and using Quip collaboration features. For Slack, this includes managing Slack app connections, user mappings, configuring features like Sales Cloud for Slack or Service Cloud for Slack, potentially managing Slack Elevate integrations. For Quip, it covers creating/managing collaborative documents, embedding Quip docs in Salesforce records, managing Quip user access, and accessing Quip metrics.
- **CPQ**: [21] [Cloud Add-Ons] Focuses on permissions related to Salesforce CPQ (Configure, Price, Quote) functionality, designed for complex product configuration and quoting processes. Permissions include managing products and price books specific to CPQ, configuring product bundles and rules (configuration, validation, pricing, alert rules), setting up discount schedules and approvals, generating quote documents, and managing contracts and renewals originating from CPQ quotes. Salesforce CPQ helps automate quoting, ensuring accuracy for complex sales.
- **Field Service**: [22] [Cloud Add-Ons] Applies to permissions for Salesforce Field Service (FSL) functionality, used to manage mobile workforce operations. Permissions cover managing service territories and resources (technicians), defining skills and availability, scheduling and dispatching service appointments (using the Dispatch Console or automation), managing work orders and service lifecycles, configuring the FSL mobile app settings, tracking inventory used in the field, and analyzing field service performance. FSL extends Service Cloud for managing on-site customer service.
- **Financial Services Cloud**: [23] [Industries] Includes permissions specific to Financial Services Cloud (FSC), tailored for banking, wealth management, and insurance industries. Permissions cover managing financial accounts, client and household relationship mapping (using the relationship map and groups), tracking financial goals and life events, managing insurance policies or claims, utilizing interaction summaries, potentially configuring compliance features (e.g., related to KYC or suitability), and accessing FSC-specific analytics.
- **Healthcare & Life Sciences Cloud**: [24] [Industries] Encompasses permissions for both Health Cloud (focused on providers, payers, patients) and Life Sciences Cloud (focused on pharma, biotech, medical device companies). For Health Cloud: managing patient data (often integrating with EHRs), care coordination tools, patient timelines, care plans, utilization management, provider network management. For Life Sciences: managing clinical trials, provider relationship management, advanced therapy management, sales programs for medical devices, regulatory compliance tracking. Both emphasize adherence to healthcare regulations.
- **Consumer Goods Cloud**: [25] [Industries] Contains permissions specific to Consumer Goods (CG) Cloud, designed for companies managing retail execution and B2B relationships in the consumer goods sector. Permissions include managing store visits, planning routes, executing in-store tasks (audits, surveys, inventory checks, planogram compliance), managing promotions and trade funds (Trade Promotion Management - TPM), handling orders specific to retail channels, account planning, and using the CG Cloud offline mobile app.
- **Communications Cloud**: [26] [Industries] Includes permissions for Communications Cloud, tailored for telecommunications and media companies. Permissions relate to managing the Enterprise Product Catalog (EPC) for complex product/service offerings, using Industries CPQ for accurate quoting of telco/media bundles, Industries Order Management (OM) for decomposing and fulfilling complex orders across systems, managing subscriber lifecycles, handling billing accounts, potentially using Digital Commerce for B2B/B2C self-service, and managing contracts.
- **Manufacturing Cloud**: [27] [Industries] Contains permissions specific to Manufacturing Cloud, aimed at connecting sales, service, and operations for manufacturers. Permissions cover managing Sales Agreements (long-term volume/price contracts), Account-Based Forecasting (combining sales forecasts with operational plans), managing partner relationships (distributors, suppliers) via Experience Cloud for Manufacturing, tracking inventory, potentially managing warranties or service parts, and utilizing manufacturing-specific analytics.
- **Nonprofit Cloud**: [28] [Industries] Includes permissions for Nonprofit Cloud, designed to meet the specific needs of nonprofit organizations. Permissions cover Fundraising features (managing donations, grants, recurring giving, payment processing), Program Management (tracking programs, services delivered, client participation), Case Management (for managing client needs and services), Outcome Management (measuring impact and mission success), potentially volunteer management, and managing marketing/engagement specific to donors and constituents.
- **General Industries Clouds**: [29] [Industries] Acts as a general category for permissions that might apply to Salesforce Industry Clouds not listed a separatecategories (such as Energy & Utilities, Public Sector). Permissions here typically involve managing industry-specific features, standard or custom objects, configuring specialized workflows or automation tailored to industry processes, managing compliance settings relevant to the sector, and utilizing industry-specific console apps or analytics.
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
| Sales Cloud                      | Cloud                 | 16    |
| Service Cloud                    | Cloud                 | 17    |
| Marking Cloud and Pardot         | Cloud                 | 18    |
| Commerce Cloud                   | Cloud                 | 19    |
| Slack and Quip                   | Cloud                 | 20    |
| CPQ                              | Cloud Add-Ons         | 21    |
| Field Service                    | Cloud Add-Ons         | 22    |
| Financial Services Cloud         | Industries            | 23    |
| Healthcare & Life Sciences Cloud | Industries            | 24    |
| Consumer Goods Cloud             | Industries            | 25    |
| Communications Cloud             | Industries            | 26    |
| Manufacturing Cloud              | Industries            | 27    |
| Nonprofit Cloud                  | Industries            | 28    |
| General Industries Cloud         | Industries            | 29    |
| UNKNOWN                          | Other                 | 99    |


# Evaluation Steps
STEP 1 - **Score Criterion** - Evaluate the permission against each criterion to obtain a **criterion match score** (1-5), noting specific matching factors.
STEP 2 - **Score Permission** - Each criterion match score is **multiplied** by its weight and **sumed** to obtain the **permission match score (weighted_score)** (round to one decimal place).  
STEP 3 - **Match Rating** - Select the best fitting category using the highest permission match ratting to assign the **Maping** to a category.
STEP 4 – **Summarize** - Aggregate findings and assess your confidence in the assigned category.  
STEP 5 - **Output** - Format the output exactly as specified in the JSON object described below—nothing else.


# Output Schema (JSON only)
```
{{
  "permission_category_label": "<General Admin|Security Admin|User Management Admin|Data Admin|Import and Export|Agentforce|Einstein and AI|Report and Dashboard|Developer|User Interface|Object Access|Data Cloud|CRM Analytics|Chatter and Communities|Shield and Event Monitoring|Sales Cloud|Service Cloud|Marking Cloud and Pardot|Commerce Cloud|Slack and Quip|CPQ|Field Service|Financial Services Cloud|Healthcare & Life Sciences Cloud|Consumer Goods Cloud|Communications Cloud|Manufacturing Cloud|Nonprofit Cloud|General Industries Cloud|UNKNOWN>",
  "permission_category_order": "<1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|99>",
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
