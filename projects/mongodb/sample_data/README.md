
# `sample_data/` Directory

This directory contains sample datasets used for demos, testing, and development of LIF services. It is part of the Polylith workspace structure, providing consistent and reusable example inputs across different components, projects, and deployment environments.

## Purpose

The `sample_data/` directory supports:
- Live product demos using curated records
- Manual and automated testing
- Reference examples for validating component behavior
- Shared input data for local development and troubleshooting

## Example Structure

Each file typically represents a validated JSON record or dataset that simulates real usage. The naming convention reflects the source or intent behind the sample.

<pre lang="markdown"> <code> 
sample_data/  
├──advisor-demo-org1/
    ├── Matt-validated.json  
    ├── Renee-validated.json  
    ├── Tracy-validated.json  
    └── Sarah-validated.json
├──advisor-demo-org2/
    ├── Jenna-validated.json  
    ├── Tracy-validated.json  
    ├── Alan-validated.json  
    └── Sarah-validated.json
├──advisor-demo-org3/
    ├── Matt-validated.json  
    ├── Jenna-validated.json  
    ├── Renee-validated.json  
    ├── Alan-validated.json  
</code> </pre>

Advisor Demo Organizations
- Advisor Demo Org1 is intended to represent an institution (State University) with the following LIF entities:
    - name
    - proficiency
    - contact
    - identifier
    - credentialAward (optional)
    - courseLearningExperience
- Advisor Demo Org2 is intended to represent a workforce organization, such as a recruiting firm, job board, or internship service with the following LIF entities:
    - name (same as Org1)
    - contact (same as Org1)
    - employmentLearningExperience
    - positionPreferences (optional)
    - employmentPreferences (optional)
- Advisor Demo Org3 is intended to represent a different institution, such as for learners with transfer credits or microcredentials (made up Summit Valley University).
    - name (same as Org1)
    - proficiency
    - contact (same as Org1)
    - identifier
    - credentialAward (optional)
    - courseLearningExperience

Files are usually structured as:
- Individual validated records
- Arrays of records for batch processing
- Service-specific formats (e.g., documents for semantic search, query records, etc.)

## Usage

You may reference these files in:
- Integration tests
- Local service runs (e.g., populating a mock database)
- UI/client previews
- QA validation steps

### Example (Python)

    import json
    
    with open("sample_data/Jenna-validated.json") as f:
        data = json.load(f)
        # Pass `data` to component or service for validation

## Guidelines

-   Keep datasets realistic but anonymized
-   Ensure files are well-formatted and valid (e.g., UTF-8, valid JSON)   
-   Avoid storing large or sensitive datasets
-   Include a README in any subdirectory if grouping data for a specific context

## Related Directories

-   `development/`: Scripts and tools that may load or consume this data
-   `components/`: Logic that may process sample data
-   `projects/`: Applications that can be run with sample inputs
