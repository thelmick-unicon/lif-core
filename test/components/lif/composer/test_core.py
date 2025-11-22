import json

from lif.composer.core import compose_with_fragment_list, compose_with_single_fragment
from lif.datatypes.core import LIFFragment, LIFRecord


employment_learning_experience_1 = '{"foo":"bar"}'
employment_learning_experience_1_dict = json.loads(employment_learning_experience_1)
employment_learning_experience_2 = '{"alpha":"beta"}'
employment_learning_experience_2_dict = json.loads(employment_learning_experience_2)
employment_learning_experience_3 = '{"gamma":"delta"}'
employment_learning_experience_3_dict = json.loads(employment_learning_experience_3)
employment_learning_experience_4 = '{"epsilon":"zeta"}'
employment_learning_experience_4_dict = json.loads(employment_learning_experience_4)
identifier_1 = '{"identifier": "100005", "identifierType": "School-assigned number"}'
identifier_1_dict = json.loads(identifier_1)
identifier_2 = '{"identifier": "sha256$81fb9410e68f70a95e9a614e8fcefba8a067fa406a1405610093713d4009844a", "identifierType": "INSTITUTION_ASSIGNED_NUMBER"}'
identifier_2_dict = json.loads(identifier_2)
identifier_3 = '{"identifier": "ABC-20250005", "identifierType": "ABC University student ID"}'
identifier_3_dict = json.loads(identifier_3)


def test_compose_with_single_fragment_with_existing_empty_array():
    lif_fragment = LIFFragment(
        fragment_path="person.employmentLearningExperience", fragment=[employment_learning_experience_1_dict]
    )
    lif_record_json = {"person": [{"foo": "foo", "employmentLearningExperience": []}]}
    lif_record = LIFRecord(**lif_record_json)
    new_lif_record = compose_with_single_fragment(lif_record, lif_fragment)
    assert lif_record.person[0]["foo"] == "foo"
    assert lif_record.person[0]["employmentLearningExperience"] == []
    assert new_lif_record.person[0]["foo"] == "foo"
    assert new_lif_record.person[0]["employmentLearningExperience"][0] == employment_learning_experience_1_dict


def test_compose_with_single_fragment_with_existing_nonempty_array():
    lif_fragment = LIFFragment(
        fragment_path="person.employmentLearningExperience", fragment=[employment_learning_experience_1_dict]
    )
    lif_record_json = {
        "person": [{"foo": "foo", "employmentLearningExperience": [employment_learning_experience_2_dict]}]
    }
    lif_record = LIFRecord(**lif_record_json)
    new_lif_record = compose_with_single_fragment(lif_record, lif_fragment)
    assert lif_record.person[0]["foo"] == "foo"
    assert lif_record.person[0]["employmentLearningExperience"] == [employment_learning_experience_2_dict]
    assert new_lif_record.person[0]["foo"] == "foo"
    assert new_lif_record.person[0]["employmentLearningExperience"][0] == employment_learning_experience_2_dict
    assert new_lif_record.person[0]["employmentLearningExperience"][1] == employment_learning_experience_1_dict


def test_compose_with_single_fragment_with_no_existing_array():
    lif_fragment = LIFFragment(
        fragment_path="person.employmentLearningExperience", fragment=[employment_learning_experience_1_dict]
    )
    lif_record_json = {"person": [{"foo": "foo"}]}
    lif_record = LIFRecord(**lif_record_json)
    new_lif_record = compose_with_single_fragment(lif_record, lif_fragment)
    assert lif_record.person[0]["foo"] == "foo"
    assert "employmentLearningExperience" not in lif_record.person[0]
    assert new_lif_record.person[0]["foo"] == "foo"
    assert new_lif_record.person[0]["employmentLearningExperience"][0] == employment_learning_experience_1_dict


def test_compose_with_fragment_list_with_existing_empty_array():
    lif_fragment1 = LIFFragment(
        fragment_path="person.employmentLearningExperience", fragment=[employment_learning_experience_1_dict]
    )
    lif_fragment2 = LIFFragment(
        fragment_path="person.employmentLearningExperience", fragment=[employment_learning_experience_2_dict]
    )
    lif_record_json = {"person": [{"foo": "foo", "employmentLearningExperience": []}]}
    lif_record = LIFRecord(**lif_record_json)
    new_lif_record = compose_with_fragment_list(lif_record, [lif_fragment1, lif_fragment2])
    assert lif_record.person[0]["foo"] == "foo"
    assert lif_record.person[0]["employmentLearningExperience"] == []
    assert new_lif_record.person[0]["foo"] == "foo"
    assert new_lif_record.person[0]["employmentLearningExperience"][0] == employment_learning_experience_1_dict
    assert new_lif_record.person[0]["employmentLearningExperience"][1] == employment_learning_experience_2_dict


def test_compose_with_fragment_list_with_existing_nonempty_array():
    lif_fragment1 = LIFFragment(
        fragment_path="person.employmentLearningExperience", fragment=[employment_learning_experience_1_dict]
    )
    lif_fragment2 = LIFFragment(
        fragment_path="person.employmentLearningExperience", fragment=[employment_learning_experience_2_dict]
    )
    lif_record_json = {
        "person": [
            {
                "foo": "foo",
                "employmentLearningExperience": [
                    employment_learning_experience_3_dict,
                    employment_learning_experience_4_dict,
                ],
            }
        ]
    }
    lif_record = LIFRecord(**lif_record_json)
    new_lif_record = compose_with_fragment_list(lif_record, [lif_fragment1, lif_fragment2])
    assert lif_record.person[0]["foo"] == "foo"
    assert lif_record.person[0]["employmentLearningExperience"] == [
        employment_learning_experience_3_dict,
        employment_learning_experience_4_dict,
    ]
    assert new_lif_record.person[0]["foo"] == "foo"
    assert new_lif_record.person[0]["employmentLearningExperience"][0] == employment_learning_experience_3_dict
    assert new_lif_record.person[0]["employmentLearningExperience"][1] == employment_learning_experience_4_dict
    assert new_lif_record.person[0]["employmentLearningExperience"][2] == employment_learning_experience_1_dict
    assert new_lif_record.person[0]["employmentLearningExperience"][3] == employment_learning_experience_2_dict


def test_compose_with_fragment_list_with_no_existing_array():
    lif_fragment3 = LIFFragment(
        fragment_path="person.employmentLearningExperience", fragment=[employment_learning_experience_3_dict]
    )
    lif_fragment4 = LIFFragment(
        fragment_path="person.employmentLearningExperience", fragment=[employment_learning_experience_4_dict]
    )
    lif_record_json = {"person": [{"foo": "foo"}]}
    lif_record = LIFRecord(**lif_record_json)
    new_lif_record = compose_with_fragment_list(lif_record, [lif_fragment3, lif_fragment4])
    assert lif_record.person[0]["foo"] == "foo"
    assert "employmentLearningExperience" not in lif_record.person[0]
    assert new_lif_record.person[0]["foo"] == "foo"
    assert new_lif_record.person[0]["employmentLearningExperience"][0] == employment_learning_experience_3_dict
    assert new_lif_record.person[0]["employmentLearningExperience"][1] == employment_learning_experience_4_dict


def test_compose_with_fragment_list_with_existing_nonempty_array_for_identifier():
    lif_fragment1 = LIFFragment(fragment_path="person.identifier", fragment=[identifier_3_dict])
    lif_record_json = {"person": [{"foo": "foo", "identifier": [identifier_1_dict, identifier_2_dict]}]}
    lif_record = LIFRecord(**lif_record_json)
    new_lif_record = compose_with_fragment_list(lif_record, [lif_fragment1])
    assert lif_record.person[0]["foo"] == "foo"
    assert lif_record.person[0]["identifier"] == [identifier_1_dict, identifier_2_dict]
    assert new_lif_record.person[0]["foo"] == "foo"
    assert new_lif_record.person[0]["identifier"][0] == identifier_1_dict
    assert new_lif_record.person[0]["identifier"][1] == identifier_2_dict
    assert new_lif_record.person[0]["identifier"][2] == identifier_3_dict


def test_compose_with_single_multi_item_fragment_with_existing_empty_array():
    lif_fragment = LIFFragment(
        fragment_path="person.employmentLearningExperience",
        fragment=[employment_learning_experience_1_dict, employment_learning_experience_2_dict],
    )
    lif_record_json = {"person": [{"foo": "foo", "employmentLearningExperience": []}]}
    lif_record = LIFRecord(**lif_record_json)
    new_lif_record = compose_with_single_fragment(lif_record, lif_fragment)
    assert lif_record.person[0]["foo"] == "foo"
    assert lif_record.person[0]["employmentLearningExperience"] == []
    assert new_lif_record.person[0]["foo"] == "foo"
    assert new_lif_record.person[0]["employmentLearningExperience"][0] == employment_learning_experience_1_dict
    assert new_lif_record.person[0]["employmentLearningExperience"][1] == employment_learning_experience_2_dict


def test_compose_with_single_multi_item_fragment_with_existing_nonempty_array():
    lif_fragment = LIFFragment(
        fragment_path="person.employmentLearningExperience",
        fragment=[employment_learning_experience_1_dict, employment_learning_experience_3_dict],
    )
    lif_record_json = {
        "person": [{"foo": "foo", "employmentLearningExperience": [employment_learning_experience_2_dict]}]
    }
    lif_record = LIFRecord(**lif_record_json)
    new_lif_record = compose_with_single_fragment(lif_record, lif_fragment)
    assert lif_record.person[0]["foo"] == "foo"
    assert lif_record.person[0]["employmentLearningExperience"] == [employment_learning_experience_2_dict]
    assert new_lif_record.person[0]["foo"] == "foo"
    assert new_lif_record.person[0]["employmentLearningExperience"][0] == employment_learning_experience_2_dict
    assert new_lif_record.person[0]["employmentLearningExperience"][1] == employment_learning_experience_1_dict
    assert new_lif_record.person[0]["employmentLearningExperience"][2] == employment_learning_experience_3_dict


def test_compose_with_single_multi_item_fragment_with_no_existing_array():
    lif_fragment = LIFFragment(
        fragment_path="person.employmentLearningExperience",
        fragment=[employment_learning_experience_1_dict, employment_learning_experience_2_dict],
    )
    lif_record_json = {"person": [{"foo": "foo"}]}
    lif_record = LIFRecord(**lif_record_json)
    new_lif_record = compose_with_single_fragment(lif_record, lif_fragment)
    assert lif_record.person[0]["foo"] == "foo"
    assert "employmentLearningExperience" not in lif_record.person[0]
    assert new_lif_record.person[0]["foo"] == "foo"
    assert new_lif_record.person[0]["employmentLearningExperience"][0] == employment_learning_experience_1_dict
    assert new_lif_record.person[0]["employmentLearningExperience"][1] == employment_learning_experience_2_dict


def test_compose_for_fragment_list_with_one_multi_item_fragment_and_lif_record_with_existing_nonempty_array():
    lif_fragment1 = LIFFragment(
        fragment_path="person.employmentLearningExperience", fragment=[employment_learning_experience_1_dict]
    )
    lif_fragment2 = LIFFragment(
        fragment_path="person.employmentLearningExperience",
        fragment=[employment_learning_experience_2_dict, employment_learning_experience_3_dict],
    )
    lif_record_json = {
        "person": [{"foo": "foo", "employmentLearningExperience": [employment_learning_experience_4_dict]}]
    }
    lif_record = LIFRecord(**lif_record_json)
    new_lif_record = compose_with_fragment_list(lif_record, [lif_fragment1, lif_fragment2])
    assert lif_record.person[0]["foo"] == "foo"
    assert lif_record.person[0]["employmentLearningExperience"] == [employment_learning_experience_4_dict]
    assert new_lif_record.person[0]["foo"] == "foo"
    assert new_lif_record.person[0]["employmentLearningExperience"][0] == employment_learning_experience_4_dict
    assert new_lif_record.person[0]["employmentLearningExperience"][1] == employment_learning_experience_1_dict
    assert new_lif_record.person[0]["employmentLearningExperience"][2] == employment_learning_experience_2_dict
    assert new_lif_record.person[0]["employmentLearningExperience"][3] == employment_learning_experience_3_dict
