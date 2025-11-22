from pydantic import ValidationError
from pytest import raises

from lif.datatypes import IdentityMapping


def test_identity_mapping_with_all_fields():
    mapping = IdentityMapping(
        mapping_id="map-123",
        lif_organization_id="org-1",
        lif_organization_person_id="person-1",
        target_system_id="ext-org-1",
        target_system_person_id="ext-person-1",
        target_system_person_id_type="SSN",
    )

    assert mapping.mapping_id == "map-123"
    assert mapping.lif_organization_id == "org-1"
    assert mapping.lif_organization_person_id == "person-1"
    assert mapping.target_system_id == "ext-org-1"
    assert mapping.target_system_person_id == "ext-person-1"
    assert mapping.target_system_person_id_type == "SSN"


def test_identity_mapping_with_empty_mapping_id():
    mapping = IdentityMapping(
        mapping_id="",
        lif_organization_id="org-1",
        lif_organization_person_id="person-1",
        target_system_id="ext-org-1",
        target_system_person_id="ext-person-1",
        target_system_person_id_type="SSN",
    )

    assert mapping.mapping_id == ""
    assert mapping.lif_organization_id == "org-1"
    assert mapping.lif_organization_person_id == "person-1"
    assert mapping.target_system_id == "ext-org-1"
    assert mapping.target_system_person_id == "ext-person-1"
    assert mapping.target_system_person_id_type == "SSN"


def test_identity_mapping_with_no_mapping_id():
    mapping = IdentityMapping(
        lif_organization_id="org-1",
        lif_organization_person_id="person-1",
        target_system_id="ext-org-1",
        target_system_person_id="ext-person-1",
        target_system_person_id_type="SSN",
    )

    assert mapping.mapping_id is None
    assert mapping.lif_organization_id == "org-1"
    assert mapping.lif_organization_person_id == "person-1"
    assert mapping.target_system_id == "ext-org-1"
    assert mapping.target_system_person_id == "ext-person-1"
    assert mapping.target_system_person_id_type == "SSN"


def test_identity_mapping_with_no_lif_organization_id():
    with raises(ValidationError) as error_info:
        IdentityMapping(
            mapping_id="map-123",
            lif_organization_person_id="person-1",
            target_system_id="ext-org-1",
            target_system_person_id="ext-person-1",
            target_system_person_id_type="SSN",
        )
    assert "lif_organization_id" in str(error_info.value)
    assert "Field required" in str(error_info.value)


def test_identity_mapping_with_no_lif_organization_person_id():
    with raises(ValidationError) as error_info:
        IdentityMapping(
            mapping_id="map-123",
            lif_organization_id="org-1",
            target_system_id="ext-org-1",
            target_system_person_id="ext-person-1",
            target_system_person_id_type="SSN",
        )
    assert "lif_organization_person_id" in str(error_info.value)
    assert "Field required" in str(error_info.value)


def test_identity_mapping_with_no_target_system_id():
    with raises(ValidationError) as error_info:
        IdentityMapping(
            mapping_id="map-123",
            lif_organization_id="org-1",
            lif_organization_person_id="person-1",
            target_system_person_id="ext-person-1",
            target_system_person_id_type="SSN",
        )
    assert "target_system_id" in str(error_info.value)
    assert "Field required" in str(error_info.value)


def test_identity_mapping_with_no_target_system_person_id():
    with raises(ValidationError) as error_info:
        IdentityMapping(
            mapping_id="map-123",
            lif_organization_id="org-1",
            lif_organization_person_id="person-1",
            target_system_id="ext-org-1",
            target_system_person_id_type="SSN",
        )
    assert "target_system_person_id" in str(error_info.value)
    assert "Field required" in str(error_info.value)


def test_identity_mapping_with_no_target_system_person_id_type():
    with raises(ValidationError) as error_info:
        IdentityMapping(
            mapping_id="map-123",
            lif_organization_id="org-1",
            lif_organization_person_id="person-1",
            target_system_id="ext-org-1",
            target_system_person_id="ext-person-1",
        )
    assert "target_system_person_id_type" in str(error_info.value)
    assert "Field required" in str(error_info.value)
