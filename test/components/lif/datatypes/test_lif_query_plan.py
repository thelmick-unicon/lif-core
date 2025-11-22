from lif.datatypes.core import LIFQueryPlan, LIFQueryPlanPart, LIFQueryPlanPartTranslation, LIFPersonIdentifier

lif_query_plan_part_1 = '{ "information_source_id": "test_source", "adapter_id": "test_adapter", "person_id": {"identifier": "12345", "identifierType": "School-assigned number"}, "lif_fragment_paths": ["person.employmentLearningExperience"]}'
lif_query_plan_part_2 = '{ "information_source_id": "test_source", "adapter_id": "test_adapter_2", "person_id": {"identifier": "67890", "identifierType": "National ID"}, "lif_fragment_paths": ["person.positionPreferences"]}'
lif_query_plan_part_3_with_translation = '{ "information_source_id": "test_source", "adapter_id": "test_adapter_2", "person_id": {"identifier": "67890", "identifierType": "National ID"}, "lif_fragment_paths": ["person.positionPreferences"], "translation": {"source_schema_id": "source_schema", "target_schema_id": "target_schema"}}'


def test_lif_query_plan_with_one_part():
    """
    Test the LIFQueryPlan model.
    """
    lif_query_plan_part = LIFQueryPlanPart(
        information_source_id="test_source",
        adapter_id="test_adapter",
        person_id=LIFPersonIdentifier(identifier="12345", identifierType="School-assigned number"),
        lif_fragment_paths=["person.employmentLearningExperience", "person.positionPreferences"],
    )

    lif_query_plan = LIFQueryPlan(root=[lif_query_plan_part])

    assert len(lif_query_plan.root) == 1
    assert lif_query_plan.root[0].adapter_id == "test_adapter"
    assert lif_query_plan.root[0].person_id.identifier == "12345"
    assert lif_query_plan.root[0].lif_fragment_paths == [
        "person.employmentLearningExperience",
        "person.positionPreferences",
    ]


def test_lif_query_plan_with_multiple_parts():
    """
    Test the LIFQueryPlan model with multiple parts.
    """
    lif_query_plan_part_1_instance = LIFQueryPlanPart(
        information_source_id="test_source",
        adapter_id="test_adapter",
        person_id=LIFPersonIdentifier(identifier="12345", identifierType="School-assigned number"),
        lif_fragment_paths=["person.employmentLearningExperience"],
    )

    lif_query_plan_part_2_instance = LIFQueryPlanPart(
        information_source_id="test_source",
        adapter_id="test_adapter_2",
        person_id=LIFPersonIdentifier(identifier="67890", identifierType="National ID"),
        lif_fragment_paths=["person.positionPreferences"],
        translation=LIFQueryPlanPartTranslation(source_schema_id="source_schema", target_schema_id="target_schema"),
    )

    lif_query_plan = LIFQueryPlan(root=[lif_query_plan_part_1_instance, lif_query_plan_part_2_instance])

    assert len(lif_query_plan.root) == 2
    assert lif_query_plan.root[0].adapter_id == "test_adapter"
    assert lif_query_plan.root[0].person_id.identifier == "12345"
    assert lif_query_plan.root[0].lif_fragment_paths == ["person.employmentLearningExperience"]

    assert lif_query_plan.root[1].adapter_id == "test_adapter_2"
    assert lif_query_plan.root[1].person_id.identifier == "67890"
    assert lif_query_plan.root[1].lif_fragment_paths == ["person.positionPreferences"]


def test_lif_query_plan_from_json():
    """
    Test creating LIFQueryPlan from JSON string.
    """
    lif_query_plan = LIFQueryPlan.model_validate_json(f"[{lif_query_plan_part_1}, {lif_query_plan_part_2}]")

    assert len(lif_query_plan.root) == 2
    assert isinstance(lif_query_plan.root[0], LIFQueryPlanPart)
    assert isinstance(lif_query_plan.root[1], LIFQueryPlanPart)
    assert isinstance(lif_query_plan.root[0].person_id, LIFPersonIdentifier)
    assert isinstance(lif_query_plan.root[1].person_id, LIFPersonIdentifier)

    assert lif_query_plan.root[0].information_source_id == "test_source"
    assert lif_query_plan.root[0].adapter_id == "test_adapter"
    assert lif_query_plan.root[0].person_id.identifier == "12345"
    assert lif_query_plan.root[0].lif_fragment_paths == ["person.employmentLearningExperience"]

    assert lif_query_plan.root[1].information_source_id == "test_source"
    assert lif_query_plan.root[1].adapter_id == "test_adapter_2"
    assert lif_query_plan.root[1].person_id.identifier == "67890"
    assert lif_query_plan.root[1].lif_fragment_paths == ["person.positionPreferences"]


def test_lif_query_plan_with_translation_from_json():
    """
    Test creating LIFQueryPlan with translation from JSON string.
    """
    lif_query_plan = LIFQueryPlan.model_validate_json(f"[{lif_query_plan_part_3_with_translation}]")

    assert len(lif_query_plan.root) == 1
    assert isinstance(lif_query_plan.root[0], LIFQueryPlanPart)
    assert isinstance(lif_query_plan.root[0].person_id, LIFPersonIdentifier)

    assert lif_query_plan.root[0].information_source_id == "test_source"
    assert lif_query_plan.root[0].adapter_id == "test_adapter_2"
    assert lif_query_plan.root[0].person_id.identifier == "67890"
    assert lif_query_plan.root[0].lif_fragment_paths == ["person.positionPreferences"]
    assert lif_query_plan.root[0].translation is not None
    assert lif_query_plan.root[0].translation.source_schema_id == "source_schema"
    assert lif_query_plan.root[0].translation.target_schema_id == "target_schema"
