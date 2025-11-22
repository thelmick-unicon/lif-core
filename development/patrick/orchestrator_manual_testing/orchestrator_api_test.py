# Use this script to make a test call to the orchestrator API
import requests

url = "http://localhost:8005/jobs"
payload = {
    "lif_query_plan": [
        {
            "adapter_identifier": "lif_adapter",
            "person_identifier": {"identifier": "100001", "identifier_type": "SCHOOL_ASSIGNED_NUMBER"},
            "lif_fragment_paths": ["person.name.firstName", "person.name.lastName"],
        }
    ]
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response Body:", response.text)
