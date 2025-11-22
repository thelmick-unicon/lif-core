from lif.datatypes.core import LIFPersonIdentifier, LIFPersonIdentifiers, LIFPerson


def test_lif_person():
    person = [{"name": "John Doe", "age": 30}]
    lif_person = LIFPerson(root=person)
    assert lif_person[0]["name"] == "John Doe"
    assert lif_person[0]["age"] == 30


def test_lif_person_with_empty_list():
    lif_person: LIFPerson = LIFPerson(root=[])
    assert lif_person.root == []


def test_lif_person_constructor_with_person_dict():
    person = {
        "person": [
            {
                "name": [{"firstName": "Jane", "lastName": "Doe"}],
                "identifier": [{"identifier": "12345", "identifier_type": "School-assigned number"}],
            }
        ]
    }
    lif_person: LIFPerson = LIFPerson(root=person["person"])
    assert lif_person[0]["identifier"][0]["identifier"] == "12345"
    assert lif_person[0]["identifier"][0]["identifier_type"] == "School-assigned number"


def test_lif_person_constructor_with_identifier_and_identifiers_list():
    lif_person_identifier: LIFPersonIdentifier = LIFPersonIdentifier(
        identifier="12345", identifierType="School-assigned number"
    )
    lif_person_identifiers: LIFPersonIdentifiers = LIFPersonIdentifiers(identifier=[lif_person_identifier])
    lif_person: LIFPerson = LIFPerson(root=[lif_person_identifiers.model_dump()])
    assert lif_person[0]["identifier"][0]["identifier"] == "12345"
    assert lif_person[0]["identifier"][0]["identifierType"] == "School-assigned number"
