# LIF Translator

The **Translator** transforms a source JSON document into a target JSON document when provided with relevant translation instructions. This component ensures that data from various source systems are appropriately translated to the **LIF Data Model** and then returns the translated JSON document.

# Example Usage
POST http://localhost:8007/translate/source/26/target/17
with body:
```json
{
    "person": {
        "id": "100001",
        "employment": {
            "preferences": {
                "preferred_org_types": ["Public Sector", "Private Sector"]
            }
        }
    }
}
```

Note that the Translator is dependent on the MDR for the transformation mappings (aka translation instructions). It is expected that the Translator will be called by the Orchestrator with the source data model ID, target data model ID, and source data as shown in the example above.