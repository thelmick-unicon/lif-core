from lif.datatypes import OrchestratorJobResults, OrchestratorJobQueryPlanPartResults, LIFFragment, LIFPersonIdentifier


orchestrator_job_results_1_json = '{ "run_id": "run_12345", "query_plan_part_results": [ { "information_source_id": "test_source_1", "adapter_id": "test_adapter_1", "data_timestamp": "2024-10-01T12:00:00Z", "person_id": {"identifier": "12345", "identifierType": "School-assigned number"}, "fragments": [ { "fragment_path": "person.positionPreferences", "fragment": [ { "informationSourceId": "Org2", "travel": [ { "percentage": 25.0, "willingToTravelIndicator": true } ], "relocation": [ { "willingToRelocateIndicator": false } ], "remoteWork": [ { "remoteWorkIndicator": true } ], "positionTitles": [ "Compliance Specialist", "Compliance Manager" ] } ] } ], "error": null }, { "information_source_id": "test_source_2", "adapter_id": "test_adapter_2", "data_timestamp": "2024-10-01T12:05:00Z", "person_id": {"identifier": "12345", "identifierType": "School-assigned number"}, "fragments": [ { "fragment_path": "person.employmentLearningExperience", "fragment": [ { "informationSourceId": "Org3", "learningExperienceType": "Course", "name": "Leadership Training", "description": "A course on leadership skills.", "startDate": "2022-01-15", "endDate": "2022-03-15", "credentialEarned": "Certificate of Completion", "issuingOrganization": { "name": "Leadership Academy", "address": { "streetAddress": "456 Leadership Rd", "addressLocality": "Anywhere", "addressRegion": "CA", "postalCode": "90210", "addressCountry": "USA" } } } ] } ],  "error": null } ] }'
orchestrator_job_results_with_error_json = '{ "run_id": "run_12345", "query_plan_part_results": [ { "information_source_id": "test_source", "adapter_id": "test_adapter", "data_timestamp": "2024-10-01T12:00:00Z", "person_id": {"identifier": "12345", "identifierType": "School-assigned number"}, "fragments": [], "error": "Failed to retrieve data" } ] }'


def test_orchestrator_job_results():
    """
    Test the OrchestratorJobResults model.
    """
    lif_fragment_1 = LIFFragment(
        fragment_path="person.positionPreferences",
        fragment=[
            {
                "informationSourceId": "Org2",
                "travel": [{"percentage": 25.0, "willingToTravelIndicator": True}],
                "relocation": [{"willingToRelocateIndicator": False}],
                "remoteWork": [{"remoteWorkIndicator": True}],
                "positionTitles": ["Compliance Specialist", "Compliance Manager"],
            }
        ],
    )

    lif_fragment_2 = LIFFragment(
        fragment_path="person.employmentLearningExperience",
        fragment=[
            {
                "informationSourceId": "Org3",
                "learningExperienceType": "Course",
                "name": "Leadership Training",
                "description": "A course on leadership skills.",
                "startDate": "2022-01-15",
                "endDate": "2022-03-15",
                "credentialEarned": "Certificate of Completion",
                "issuingOrganization": {
                    "name": "Leadership Academy",
                    "address": {
                        "streetAddress": "456 Leadership Rd",
                        "addressLocality": "Anywhere",
                        "addressRegion": "CA",
                        "postalCode": "90210",
                        "addressCountry": "USA",
                    },
                },
            }
        ],
    )

    person_id = LIFPersonIdentifier(identifier="12345", identifierType="School-assigned number")

    orchestrator_job_query_plan_part_results_1 = OrchestratorJobQueryPlanPartResults(
        information_source_id="test_source_1",
        adapter_id="test_adapter_1",
        data_timestamp="2024-10-01T12:00:00Z",
        person_id=person_id,
        fragments=[lif_fragment_1],
        error=None,
    )

    orchestrator_job_query_plan_part_results_2 = OrchestratorJobQueryPlanPartResults(
        information_source_id="test_source_2",
        adapter_id="test_adapter_2",
        data_timestamp="2024-10-01T12:05:00Z",
        person_id=person_id,
        fragments=[lif_fragment_2],
        error=None,
    )

    orchestrator_job_results = OrchestratorJobResults(
        run_id="run_12345",
        query_plan_part_results=[
            orchestrator_job_query_plan_part_results_1,
            orchestrator_job_query_plan_part_results_2,
        ],
    )

    assert orchestrator_job_results.run_id == "run_12345"
    assert len(orchestrator_job_results.query_plan_part_results) == 2
    assert orchestrator_job_results.query_plan_part_results[0].information_source_id == "test_source_1"
    assert orchestrator_job_results.query_plan_part_results[0].person_id.identifier == "12345"
    assert orchestrator_job_results.query_plan_part_results[0].person_id.identifierType == "School-assigned number"
    assert orchestrator_job_results.query_plan_part_results[1].information_source_id == "test_source_2"
    assert orchestrator_job_results.query_plan_part_results[1].person_id.identifier == "12345"
    assert orchestrator_job_results.query_plan_part_results[1].person_id.identifierType == "School-assigned number"
    assert len(orchestrator_job_results.query_plan_part_results[0].fragments) == 1
    assert len(orchestrator_job_results.query_plan_part_results[1].fragments) == 1
    assert (
        orchestrator_job_results.query_plan_part_results[0].fragments[0].fragment_path == "person.positionPreferences"
    )
    assert (
        orchestrator_job_results.query_plan_part_results[1].fragments[0].fragment_path
        == "person.employmentLearningExperience"
    )
    assert orchestrator_job_results.query_plan_part_results[0].error is None
    assert orchestrator_job_results.query_plan_part_results[1].error is None


def test_orchestrator_job_results_with_error_and_no_fragments():
    """
    Test the OrchestratorJobResults model with no fragments.
    """
    orchestrator_job_query_plan_part_results = OrchestratorJobQueryPlanPartResults(
        information_source_id="test_source",
        adapter_id="test_adapter",
        data_timestamp="2024-10-01T12:00:00Z",
        person_id=LIFPersonIdentifier(identifier="12345", identifierType="School-assigned number"),
        fragments=[],
        error="Failed to retrieve data",
    )

    orchestrator_job_results = OrchestratorJobResults(
        run_id="run_12345", query_plan_part_results=[orchestrator_job_query_plan_part_results]
    )

    assert orchestrator_job_results.run_id == "run_12345"
    assert orchestrator_job_results.query_plan_part_results[0].person_id.identifier == "12345"
    assert orchestrator_job_results.query_plan_part_results[0].person_id.identifierType == "School-assigned number"
    assert len(orchestrator_job_results.query_plan_part_results) == 1
    assert orchestrator_job_results.query_plan_part_results[0].information_source_id == "test_source"
    assert len(orchestrator_job_results.query_plan_part_results[0].fragments) == 0
    assert orchestrator_job_results.query_plan_part_results[0].error == "Failed to retrieve data"


def test_orchestrator_job_results_from_json():
    """
    Test creating OrchestratorJobResults from JSON string.
    """
    orchestrator_job_results = OrchestratorJobResults.model_validate_json(orchestrator_job_results_1_json)

    assert orchestrator_job_results.run_id == "run_12345"
    assert len(orchestrator_job_results.query_plan_part_results) == 2

    orchestrator_job_query_plan_part_results = orchestrator_job_results.query_plan_part_results[0]
    assert orchestrator_job_query_plan_part_results.person_id.identifier == "12345"
    assert orchestrator_job_query_plan_part_results.person_id.identifierType == "School-assigned number"
    assert orchestrator_job_query_plan_part_results.information_source_id == "test_source_1"
    assert orchestrator_job_query_plan_part_results.adapter_id == "test_adapter_1"
    assert orchestrator_job_query_plan_part_results.data_timestamp == "2024-10-01T12:00:00Z"
    assert len(orchestrator_job_query_plan_part_results.fragments) == 1
    fragment_1 = orchestrator_job_query_plan_part_results.fragments[0]
    assert fragment_1.fragment_path == "person.positionPreferences"
    assert len(fragment_1.fragment) == 1
    assert fragment_1.fragment[0]["informationSourceId"] == "Org2"
    assert len(fragment_1.fragment[0]["travel"]) == 1
    assert fragment_1.fragment[0]["travel"][0]["percentage"] == 25.0
    assert fragment_1.fragment[0]["travel"][0]["willingToTravelIndicator"] is True
    assert len(fragment_1.fragment[0]["relocation"]) == 1
    assert fragment_1.fragment[0]["relocation"][0]["willingToRelocateIndicator"] is False
    assert len(fragment_1.fragment[0]["remoteWork"]) == 1
    assert fragment_1.fragment[0]["remoteWork"][0]["remoteWorkIndicator"] is True
    assert fragment_1.fragment[0]["positionTitles"] == ["Compliance Specialist", "Compliance Manager"]
    assert orchestrator_job_query_plan_part_results.error is None

    orchestrator_job_query_plan_part_results_2 = orchestrator_job_results.query_plan_part_results[1]
    assert orchestrator_job_query_plan_part_results_2.information_source_id == "test_source_2"
    assert orchestrator_job_query_plan_part_results_2.adapter_id == "test_adapter_2"
    assert orchestrator_job_query_plan_part_results_2.data_timestamp == "2024-10-01T12:05:00Z"
    assert len(orchestrator_job_query_plan_part_results_2.fragments) == 1
    fragment_2 = orchestrator_job_query_plan_part_results_2.fragments[0]
    assert fragment_2.fragment_path == "person.employmentLearningExperience"
    assert len(fragment_2.fragment) == 1
    learning_experience = fragment_2.fragment[0]
    assert learning_experience["informationSourceId"] == "Org3"
    assert learning_experience["learningExperienceType"] == "Course"
    assert learning_experience["name"] == "Leadership Training"
    assert learning_experience["description"] == "A course on leadership skills."
    assert learning_experience["startDate"] == "2022-01-15"
    assert learning_experience["endDate"] == "2022-03-15"
    assert learning_experience["credentialEarned"] == "Certificate of Completion"
    assert learning_experience["issuingOrganization"]["name"] == "Leadership Academy"
    assert learning_experience["issuingOrganization"]["address"]["streetAddress"] == "456 Leadership Rd"
    assert learning_experience["issuingOrganization"]["address"]["addressLocality"] == "Anywhere"
    assert learning_experience["issuingOrganization"]["address"]["addressRegion"] == "CA"
    assert learning_experience["issuingOrganization"]["address"]["postalCode"] == "90210"
    assert learning_experience["issuingOrganization"]["address"]["addressCountry"] == "USA"
    assert orchestrator_job_query_plan_part_results_2.error is None


def test_orchestrator_job_results_with_error_and_no_fragments_from_json():
    """
    Test creating OrchestratorJobResults with no fragments from JSON string.
    """
    orchestrator_job_results = OrchestratorJobResults.model_validate_json(orchestrator_job_results_with_error_json)

    assert orchestrator_job_results.run_id == "run_12345"
    assert len(orchestrator_job_results.query_plan_part_results) == 1

    orchestrator_job_query_plan_part_results = orchestrator_job_results.query_plan_part_results[0]
    assert orchestrator_job_query_plan_part_results.person_id.identifier == "12345"
    assert orchestrator_job_query_plan_part_results.person_id.identifierType == "School-assigned number"
    assert orchestrator_job_query_plan_part_results.information_source_id == "test_source"
    assert orchestrator_job_query_plan_part_results.adapter_id == "test_adapter"
    assert orchestrator_job_query_plan_part_results.data_timestamp == "2024-10-01T12:00:00Z"
    assert len(orchestrator_job_query_plan_part_results.fragments) == 0
    assert orchestrator_job_query_plan_part_results.error == "Failed to retrieve data"
