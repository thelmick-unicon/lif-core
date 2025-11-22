from lif.datatypes.core import LIFRecord


def test_lif_record():
    person = {"person": [{"name": "John Doe", "age": 30}]}
    lif_record = LIFRecord(**person)
    assert lif_record.person[0]["name"] == "John Doe"
    assert lif_record.person[0]["age"] == 30


def test_lif_record_with_empty_person():
    person = {"person": []}
    lif_record = LIFRecord(**person)
    assert lif_record.person.root == []


def test_lif_record_constructor_with_no_person_throws_value_error():
    try:
        LIFRecord()
    except ValueError as e:
        assert "Field required" in str(e)


def test_lif_record_constructor_with_identifiers_list():
    person = {
        "person": [
            {
                "name": [{"firstName": "Jane", "lastName": "Doe"}],
                "identifier": [{"identifier": "12345", "identifier_type": "School-assigned number"}],
            }
        ]
    }
    lif_record = LIFRecord(**person)
    assert lif_record.person[0]["identifier"][0]["identifier"] == "12345"
    assert lif_record.person[0]["identifier"][0]["identifier_type"] == "School-assigned number"
