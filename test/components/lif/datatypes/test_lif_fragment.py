from lif.datatypes.core import LIFFragment


def test_lif_fragment():
    fragment = LIFFragment(fragment_path="person.employmentLearningExperience", fragment=[{"foo": "bar"}])
    assert fragment.fragment_path == "person.employmentLearningExperience"
    assert fragment.fragment == [{"foo": "bar"}]


def test_lif_fragment_with_no_fragment_path_throws_value_error():
    try:
        LIFFragment(fragment=[{"foo": "bar"}])
    except ValueError as e:
        assert "Field required" in str(e)


def test_lif_fragment_with_empty_fragment_path_throws_value_error():
    try:
        LIFFragment(fragment_path="", fragment=[{"foo": "bar"}])
    except ValueError as e:
        assert "No fragment_path provided." in str(e)


def test_lif_fragment_with_path_without_proper_prefix_throws_value_error():
    try:
        LIFFragment(fragment_path="$.person[0].employmentLearningExperience", fragment=[{"foo": "bar"}])
    except ValueError as e:
        assert "Fragment path must start with 'person." in str(e)


def test_lif_fragment_with_no_fragment_throws_value_error():
    try:
        LIFFragment(fragment_path="person.employmentLearningExperience")
    except ValueError as e:
        assert "Field required" in str(e)


def test_lif_fragment_with_no_fragment_list_entries_throws_value_error():
    try:
        LIFFragment(fragment_path="person.employmentLearningExperience", fragment=[])
    except ValueError as e:
        assert "No fragment entries provided" in str(e)


def test_lif_fragment_with_non_dictionary_fragment_list_entry_throws_value_error():
    try:
        LIFFragment(fragment_path="$.person[0].employmentLearningExperience", fragment=["str"])
    except ValueError as e:
        assert "Input should be a valid dictionary" in str(e)
