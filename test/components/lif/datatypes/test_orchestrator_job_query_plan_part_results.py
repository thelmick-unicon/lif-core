from lif.datatypes import OrchestratorJobQueryPlanPartResults, LIFFragment, LIFPersonIdentifier


def test_orchestrator_job_query_plan_part_results_with_single_fragment():
    """
    Test the OrchestratorJobQueryPlanPartResults model.
    """
    lif_fragment = LIFFragment(
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

    orchestrator_job_query_plan_part_results = OrchestratorJobQueryPlanPartResults(
        information_source_id="test_source",
        adapter_id="test_adapter",
        data_timestamp="2024-10-01T12:00:00Z",
        person_id=LIFPersonIdentifier(identifier="12345", identifierType="School-assigned number"),
        fragments=[lif_fragment],
        error=None,
    )

    assert orchestrator_job_query_plan_part_results.information_source_id == "test_source"
    assert orchestrator_job_query_plan_part_results.adapter_id == "test_adapter"
    assert orchestrator_job_query_plan_part_results.data_timestamp == "2024-10-01T12:00:00Z"
    assert orchestrator_job_query_plan_part_results.person_id.identifier == "12345"
    assert orchestrator_job_query_plan_part_results.person_id.identifierType == "School-assigned number"
    assert len(orchestrator_job_query_plan_part_results.fragments) == 1
    assert orchestrator_job_query_plan_part_results.fragments[0].fragment_path == "person.positionPreferences"
    assert len(orchestrator_job_query_plan_part_results.fragments[0].fragment) == 1
    assert orchestrator_job_query_plan_part_results.fragments[0].fragment[0]["informationSourceId"] == "Org2"
    assert len(orchestrator_job_query_plan_part_results.fragments[0].fragment[0]["travel"]) == 1
    assert orchestrator_job_query_plan_part_results.fragments[0].fragment[0]["travel"][0]["percentage"] == 25.0
    assert (
        orchestrator_job_query_plan_part_results.fragments[0].fragment[0]["travel"][0]["willingToTravelIndicator"]
        is True
    )
    assert len(orchestrator_job_query_plan_part_results.fragments[0].fragment[0]["relocation"]) == 1
    assert (
        orchestrator_job_query_plan_part_results.fragments[0].fragment[0]["relocation"][0]["willingToRelocateIndicator"]
        is False
    )
    assert len(orchestrator_job_query_plan_part_results.fragments[0].fragment[0]["remoteWork"]) == 1
    assert (
        orchestrator_job_query_plan_part_results.fragments[0].fragment[0]["remoteWork"][0]["remoteWorkIndicator"]
        is True
    )
    assert orchestrator_job_query_plan_part_results.fragments[0].fragment[0]["positionTitles"] == [
        "Compliance Specialist",
        "Compliance Manager",
    ]
    assert orchestrator_job_query_plan_part_results.error is None


def test_orchestrator_job_query_plan_part_results_with_multiple_fragments():
    """
    Test the OrchestratorJobQueryPlanPartResults model with multiple fragments.
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
                "learningExperiences": [
                    {
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
            }
        ],
    )

    orchestrator_job_query_plan_part_results = OrchestratorJobQueryPlanPartResults(
        information_source_id="test_source",
        adapter_id="test_adapter",
        data_timestamp="2024-10-01T12:00:00Z",
        person_id=LIFPersonIdentifier(identifier="12345", identifierType="School-assigned number"),
        fragments=[lif_fragment_1, lif_fragment_2],
        error=None,
    )

    assert orchestrator_job_query_plan_part_results.information_source_id == "test_source"
    assert orchestrator_job_query_plan_part_results.adapter_id == "test_adapter"
    assert orchestrator_job_query_plan_part_results.data_timestamp == "2024-10-01T12:00:00Z"
    assert orchestrator_job_query_plan_part_results.person_id.identifier == "12345"
    assert orchestrator_job_query_plan_part_results.person_id.identifierType == "School-assigned number"
    assert len(orchestrator_job_query_plan_part_results.fragments) == 2

    # Validate first fragment
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
    # Validate second fragment
    fragment_2 = orchestrator_job_query_plan_part_results.fragments[1]
    assert fragment_2.fragment_path == "person.employmentLearningExperience"
    assert len(fragment_2.fragment) == 1
    assert fragment_2.fragment[0]["informationSourceId"] == "Org3"
    assert len(fragment_2.fragment[0]["learningExperiences"]) == 1
    learning_experience = fragment_2.fragment[0]["learningExperiences"][0]
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
    assert orchestrator_job_query_plan_part_results.error is None


def test_orchestrator_job_query_plan_part_results_with_error():
    """
    Test the OrchestratorJobQueryPlanPartResults model with an error.
    """
    orchestrator_job_query_plan_part_results = OrchestratorJobQueryPlanPartResults(
        information_source_id="test_source",
        adapter_id="test_adapter",
        data_timestamp="2024-10-01T12:00:00Z",
        person_id=LIFPersonIdentifier(identifier="12345", identifierType="School-assigned number"),
        fragments=[],
        error="Test error message",
    )

    assert orchestrator_job_query_plan_part_results.information_source_id == "test_source"
    assert orchestrator_job_query_plan_part_results.adapter_id == "test_adapter"
    assert orchestrator_job_query_plan_part_results.data_timestamp == "2024-10-01T12:00:00Z"
    assert orchestrator_job_query_plan_part_results.person_id.identifier == "12345"
    assert orchestrator_job_query_plan_part_results.person_id.identifierType == "School-assigned number"
    assert len(orchestrator_job_query_plan_part_results.fragments) == 0
    assert orchestrator_job_query_plan_part_results.error == "Test error message"
