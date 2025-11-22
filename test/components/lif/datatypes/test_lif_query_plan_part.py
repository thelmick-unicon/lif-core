from lif.datatypes.core import LIFQueryPlanPart, LIFPersonIdentifier

lif_query_plan_part_1 = '{ "information_source_id": "test_source", "adapter_id": "test_adapter", "person_id": {"identifier": "12345", "identifierType": "School-assigned number"}, "lif_fragment_paths": ["person.employmentLearningExperience"]}'


def test_lif_query_plan_part():
    """
    Test the LIFQueryPlanPart model.
    """
    lif_query_plan_part = LIFQueryPlanPart(
        information_source_id="test_source",
        adapter_id="test_adapter",
        person_id=LIFPersonIdentifier(identifier="12345", identifierType="School-assigned number"),
        lif_fragment_paths=["person.employmentLearningExperience", "person.positionPreferences"],
    )

    assert lif_query_plan_part.information_source_id == "test_source"
    assert lif_query_plan_part.adapter_id == "test_adapter"
    assert lif_query_plan_part.person_id.identifier == "12345"
    assert lif_query_plan_part.person_id.identifierType == "School-assigned number"
    assert lif_query_plan_part.lif_fragment_paths == [
        "person.employmentLearningExperience",
        "person.positionPreferences",
    ]


def test_lif_query_plan_part_from_json():
    """
    Test creating LIFQueryPlanPart from JSON string.
    """
    lif_query_plan_part = LIFQueryPlanPart.model_validate_json(lif_query_plan_part_1)

    assert lif_query_plan_part.information_source_id == "test_source"
    assert lif_query_plan_part.adapter_id == "test_adapter"
    assert lif_query_plan_part.person_id.identifier == "12345"
    assert lif_query_plan_part.person_id.identifierType == "School-assigned number"
    assert lif_query_plan_part.lif_fragment_paths == ["person.employmentLearningExperience"]
