from typing import List

from lif.datatypes import IdentityMapping
from lif.exceptions.core import DataStoreException
from lif.identity_mapper_storage.core import IdentityMapperStorage
from lif.identity_mapper_storage_sql.model import IdentityMappingModel
from lif.identity_mapper_storage_sql.crud import (
    create,
    read,
    update,
    delete,
    read_by_lif_org_and_person,
    read_by_lif_org_and_person_and_target_system_and_target_system_person_id_type,
)


class IdentityMapperSqlStorage(IdentityMapperStorage):
    """
    An implementation of IdentityMapperStorage that uses an SQL database for data storage.
    """

    def __init__(self, db_session_factory):
        self.db_session_factory = db_session_factory

    async def get_mapping_by_id(self, mapping_id: str) -> IdentityMapping | None:
        """
        Retrieve an identity mapping by its ID.
        Returns None if the mapping does not exist.
        Raises DataStoreException for database-related errors.
        """
        try:
            with self.db_session_factory() as session:
                with session.begin():
                    mapping_model: IdentityMappingModel | None = read(session, mapping_id)
                    if mapping_model:
                        return IdentityMapping.model_validate(mapping_model)
                    else:
                        return None
        except Exception as e:
            raise DataStoreException from e

    async def get_mappings(self, lif_organization_id: str, lif_organization_person_id: str) -> List[IdentityMapping]:
        """
        Retrieve identity mappings for a person in a LIF organization.
        Raises DataStoreException for database-related errors.
        """
        try:
            with self.db_session_factory() as session:
                with session.begin():
                    mapping_models: List[IdentityMappingModel] = read_by_lif_org_and_person(
                        session, lif_organization_id, lif_organization_person_id
                    )
                    return [IdentityMapping.model_validate(mapping_model) for mapping_model in mapping_models]
        except Exception as e:
            raise DataStoreException from e

    async def save_mapping(self, identity_mapping: IdentityMapping) -> IdentityMapping:
        try:
            with self.db_session_factory() as session:
                with session.begin():
                    mapping_id: str | None = identity_mapping.mapping_id
                    org_id: str = identity_mapping.lif_organization_id
                    person_id: str = identity_mapping.lif_organization_person_id
                    target_system_id: str = identity_mapping.target_system_id
                    target_system_person_id: str = identity_mapping.target_system_person_id
                    target_system_person_id_type: str = identity_mapping.target_system_person_id_type

                    existing: IdentityMappingModel | None = (
                        read_by_lif_org_and_person_and_target_system_and_target_system_person_id_type(
                            session, org_id, person_id, target_system_id, target_system_person_id_type
                        )
                        if mapping_id is None
                        else read(session, mapping_id)
                    )
                    if existing is None:
                        mapping_model = IdentityMappingModel()
                        mapping_model.from_identity_mapping(identity_mapping)
                        created: IdentityMappingModel = create(session, mapping_model)
                        return IdentityMapping.model_validate(created)
                    elif existing.target_system_person_id == target_system_person_id:
                        return IdentityMapping.model_validate(existing)  # nothing to update
                    else:
                        existing.target_system_person_id = target_system_person_id
                        updated: IdentityMappingModel = update(session, existing)
                        return IdentityMapping.model_validate(updated)
        except Exception as e:
            raise DataStoreException from e

    async def delete_mapping_by_id(self, mapping_id: str) -> IdentityMapping | None:
        """
        Delete the identity mapping identified by the mapping_id.
        Returns the deleted IdentityMapping, or None if it did not exist.
        Raises DataStoreException for database-related errors.
        """
        try:
            existing: IdentityMapping | None = await self.get_mapping_by_id(mapping_id)
            if existing is None:
                return None
            else:
                with self.db_session_factory() as session:
                    with session.begin():
                        delete(session, mapping_id)
                return existing
        except Exception as e:
            raise DataStoreException from e
