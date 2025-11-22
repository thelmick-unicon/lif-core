from unittest.mock import AsyncMock, Mock
import pytest

from lif.datatypes import IdentityMapping
from lif.exceptions.core import DataNotFoundException, DataStoreException
from lif.identity_mapper_service.core import IdentityMapperService
from lif.identity_mapper_storage.core import IdentityMapperStorage


def test_service_initialization():
    storage: IdentityMapperStorage = AsyncMock()
    service = IdentityMapperService(storage=storage)
    assert service.storage == storage


@pytest.mark.asyncio
async def test_get_mappings_with_no_mappings():
    storage: IdentityMapperStorage = Mock()
    storage.get_mappings = AsyncMock(return_value=[])
    service = IdentityMapperService(storage=storage)
    result = await service.get_mappings("org-1", "person-1")
    assert result == []
    storage.get_mappings.assert_called_once_with("org-1", "person-1")


@pytest.mark.asyncio
async def test_get_mappings_with_mappings():
    mappings = [
        IdentityMapping(
            mapping_id="test-id-1",
            lif_organization_id="org-1",
            lif_organization_person_id="person-1",
            target_system_id="ext-org-1",
            target_system_person_id_type="School-assigned number",
            target_system_person_id="ext-person-1",
        ),
        IdentityMapping(
            mapping_id="test-id-2",
            lif_organization_id="org-1",
            lif_organization_person_id="person-1",
            target_system_id="ext-org-2",
            target_system_person_id_type="School-assigned number",
            target_system_person_id="ext-person-2",
        ),
    ]
    storage: IdentityMapperStorage = Mock()
    storage.get_mappings = AsyncMock(return_value=mappings)
    service = IdentityMapperService(storage=storage)
    result = await service.get_mappings("org-1", "person-1")
    assert result == mappings
    storage.get_mappings.assert_called_once_with("org-1", "person-1")


@pytest.mark.asyncio
async def test_get_mappings_when_storage_raises_exception():
    storage: IdentityMapperStorage = Mock()
    storage.get_mappings = AsyncMock(side_effect=Exception("Database error"))
    service = IdentityMapperService(storage=storage)
    try:
        await service.get_mappings("org-1", "person-1")
        assert False, "Expected exception was not raised"
    except Exception as e:
        assert str(e) == "Database error"
    storage.get_mappings.assert_called_once_with("org-1", "person-1")


@pytest.mark.asyncio
async def test_save_mappings_success():
    mappings = [
        IdentityMapping(
            mapping_id=None,
            lif_organization_id="org-1",
            lif_organization_person_id="person-1",
            target_system_id="ext-org-1",
            target_system_person_id_type="School-assigned number",
            target_system_person_id="ext-person-1",
        ),
        IdentityMapping(
            mapping_id=None,
            lif_organization_id="org-1",
            lif_organization_person_id="person-1",
            target_system_id="ext-org-2",
            target_system_person_id_type="School-assigned number",
            target_system_person_id="ext-person-2",
        ),
    ]

    saved_mappings = [
        IdentityMapping(
            mapping_id="saved-id-1",
            lif_organization_id="org-1",
            lif_organization_person_id="person-1",
            target_system_id="ext-org-1",
            target_system_person_id_type="School-assigned number",
            target_system_person_id="ext-person-1",
        ),
        IdentityMapping(
            mapping_id="saved-id-2",
            lif_organization_id="org-1",
            lif_organization_person_id="person-1",
            target_system_id="ext-org-2",
            target_system_person_id_type="School-assigned number",
            target_system_person_id="ext-person-2",
        ),
    ]

    storage: IdentityMapperStorage = Mock()
    storage.save_mapping = AsyncMock(side_effect=saved_mappings)
    service = IdentityMapperService(storage=storage)
    result = await service.save_mappings("org-1", "person-1", mappings)
    assert result == saved_mappings
    assert storage.save_mapping.call_count == 2
    storage.save_mapping.assert_any_call(mappings[0])
    storage.save_mapping.assert_any_call(mappings[1])


@pytest.mark.asyncio
async def test_delete_mapping_success():
    storage: IdentityMapperStorage = Mock()
    storage.get_mapping_by_id = AsyncMock(
        side_effect=[
            IdentityMapping(
                mapping_id="mapping-id-1",
                lif_organization_id="org-1",
                lif_organization_person_id="person-1",
                target_system_id="ext-org-1",
                target_system_person_id_type="School-assigned number",
                target_system_person_id="ext-person-1",
            ),
            None,
        ]
    )
    storage.delete_mapping_by_id = AsyncMock(return_value=None)
    service = IdentityMapperService(storage=storage)
    result = await service.delete_mapping("org-1", "person-1", "mapping-id-1")
    assert result is None
    storage.delete_mapping_by_id.assert_called_once_with("mapping-id-1")


@pytest.mark.asyncio
async def test_delete_mapping_when_mapping_not_found():
    storage: IdentityMapperStorage = Mock()
    storage.get_mapping_by_id = AsyncMock(side_effect=[None])
    storage.delete_mapping_by_id = AsyncMock(return_value=None)
    service = IdentityMapperService(storage=storage)
    try:
        await service.delete_mapping("org-1", "person-1", "non-existent-id")
        assert False, "Expected DataNotFoundException was not raised"
    except DataNotFoundException as e:
        assert str(e) == "Mapping not found for ID: non-existent-id"


@pytest.mark.asyncio
async def test_delete_mapping_when_storage_raises_exception():
    mapping_id = "mapping-id-1"
    storage: IdentityMapperStorage = Mock()
    storage.get_mapping_by_id = AsyncMock(
        side_effect=[
            IdentityMapping(
                mapping_id=mapping_id,
                lif_organization_id="org-1",
                lif_organization_person_id="person-1",
                target_system_id="ext-org-1",
                target_system_person_id_type="School-assigned number",
                target_system_person_id="ext-person-1",
            ),
            None,
        ]
    )
    storage.delete_mapping_by_id = AsyncMock(side_effect=DataStoreException("Database error."))
    service = IdentityMapperService(storage=storage)
    try:
        await service.delete_mapping("org-1", "person-1", "mapping-id-1")
        assert False, "Expected DataStoreException was not raised"
    except DataStoreException as e:
        assert str(e) == "Database error."
    storage.delete_mapping_by_id.assert_called_once_with("mapping-id-1")
