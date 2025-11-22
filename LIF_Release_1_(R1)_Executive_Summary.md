
# LIF Release 1 (R1) – Executive Summary

## Overview

Release 1 delivers the foundation of the LIF platform. It connects core components, integrates the Metadata Repository (MDR), and enables the first end-to-end orchestration of learner data using a mock source system. This release is designed to demonstrate functionality and provide a base for iterative improvements, rather than serving as a production-ready system.

The core LIF components remain in place, and they continue to evolve in response to community feedback and emerging technologies such as Model Context Protocol (MCP). 

Several areas of feedback have shaped our latest updates.

-   First, we are addressing performance concerns by streamlining data flows and adding new architectural options to make the system more efficient.
    
-   Second, we are building in greater support for individual learners, ensuring that the framework not only connects institutional systems but also empowers people directly.
    
-   Third, we are working to improve access to exploring the model, making it easier for both technical and non-technical users to understand and engage with the data structures that power LIF.
    

## Key Highlights

-   **Core Infrastructure:** Initial adapter and orchestration pipelines in place.
    
    -   The Orchestrator has been decomposed into smaller parts, so organizations can customize their implementations and using only what components they need
        
    -   A new Persistent Cache has been added to improve performance and provide memory across interactions.
        
    -   The Translator is now going to be powered by JSONata translation instructions instead of Jinja, decreasing complexity and improving performance.
        
-   **New Metadata Repository (MDR):** offers a user-friendly interface for exploring the LIF data model and mapping its connections to other data sets,
    
    -   **Data Rules:** A Set of rules has been established to ensure consistency of the data types and formatting of the data model.
        
    -   **MDR Integration:** The MDR is now the system of record for metadata, powering the GraphQL API and Query Planner.
        
    -   **Data Model Explorer Enhancements:** Usability fixes and improved labeling.
        
-   **MCP-based Connector:** initial connector available to connect LIF data to large language models (LLMs)
    
-   **Mock Source Deployment:** AWS-hosted mock data source provides test data for demonstrations.
    
-   **Governance:** Codebase restructured with updated documentation and released under Apache 2.0.
    

## Design Choices

-   **MDR-Centric:** All components now align to MDR as the authoritative source of metadata.
    
-   **AWS Mock Environment:** Demonstration-focused, not production-ready.
    
-   **MVP Scope:** Features limited to single-source orchestration and baseline GraphQL queries.
    

## Known Limitations

-   Orchestration is limited to single data source queries and experiences latency
    
-   Some MDR functionality (e.g., reuse and audit improvements) remains incomplete.
    
-   GraphQL API currently supports a narrow set of queries.
    
-   Documentation and design decisions are still being built out.
    
-   Data Model Explorer retains some bugs and export limitations.
    
-   Public endpoints for MDR have not been secured yet.
    

## What’s Next

The following features and improvements are not part of this release but are planned for Release 1.1: Mid-November

-   **Orchestration & Ops:** Engine/UI refinements, partial-success handling, Dagster CI/CD, removal of cold starts.
    
-   **Async & Performance:** Async workflows, cache performance improvements, faster logout.
    
-   **Identity Mapper & Query Planner:** Full deployment and integration into orchestration.
    
-   **GraphQL & Adapters:** Multi-learner queries, dynamic GraphQL generation, adapter improvements.
    
-   **MDR Enhancements:** Schema upload/update via UI, cleaner DB restore, endpoint cleanup, unit test coverage, exclusion of deprecated entities/attributes.
    
-   **Data Model Quality:** Broader audits, parity checks, and capture of common extensions.
    
-   **MCP Guardrails:** Prompt tuning and stronger LLM safeguards.
    
-   **Other:** Clarifications on Partner LIF Pub/Inc behavior; formal adapter documentation.
    

## Usage Guidance

-   Use the AWS-hosted mock system for demos and exploration.
    
-   This early release provides core functionality only; documentation will be expanded in future updates.
    
- This release is targeted for previous LIF community members, not a public release.
    
-   Feedback from users is essential to inform the priorities for future releases.
    
-   Link here with GitHub access instructions, contact info, etc? Release is not “production ready”
    

## Looking Ahead

The next release will expand orchestration to multiple sources, iterate on Identity Mapper functionality, refine included MDR schemas, and refine the user experience across the platform.

LIF community groups will identify and inform development priorities post Release 1.1 in November. The community groups will be focused on 3 different uses, including contextual data for generative AI, Learner Wallets, and eTranscripts for dual enrollment. To participate in these groups sign up [using this link](https://forms.gle/735gNJhtB63paqi7A).
