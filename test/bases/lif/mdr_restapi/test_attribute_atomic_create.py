"""Atomic create-attribute (Issue #1028).

Passing ``EntityId`` to ``create_attribute`` must create the attribute AND its
entity association in a single transaction, so a dropped response can never leave
an orphaned (persisted-but-unassociated) attribute. Without ``EntityId`` the
behaviour is unchanged (attribute only, no association).

Drives the real service against a live Postgres (``test_db_session`` fixture).
"""

from sqlmodel import select

from lif.datatypes.mdr_sql_model import DataModel, DataModelType, Entity, EntityAttributeAssociation
from lif.mdr_dto.attribute_dto import CreateAttributeDTO
from lif.mdr_services.attribute_service import create_attribute


async def _seed_model_and_entity(session, tag):
    # Unique names per test — the fixture DB is shared across tests in this module.
    dm = DataModel(
        Name=f"AtomicCreateDM_{tag}",
        Type=DataModelType.SourceSchema,
        DataModelVersion="1.0",
        ContributorOrganization="UniconQA",
        Deleted=False,
    )
    session.add(dm)
    await session.commit()
    await session.refresh(dm)

    name = f"Widget_{tag}"
    entity = Entity(Name=name, UniqueName=name, DataModelId=dm.Id, Array="No", Required="No", Deleted=False)
    session.add(entity)
    await session.commit()
    await session.refresh(entity)
    return dm, entity


async def _associations_for(session, attribute_id):
    result = await session.execute(
        select(EntityAttributeAssociation).where(
            EntityAttributeAssociation.AttributeId == attribute_id,
            EntityAttributeAssociation.Deleted == False,  # noqa: E712
        )
    )
    return result.scalars().all()


async def test_create_attribute_with_entity_id_creates_association_atomically(test_db_session):
    session = test_db_session
    dm, entity = await _seed_model_and_entity(session, "assoc")

    created = await create_attribute(
        session,
        CreateAttributeDTO(
            Name="color",
            UniqueName=f"{entity.UniqueName}.color",
            DataType="xsd:string",
            DataModelId=dm.Id,
            EntityId=entity.Id,
        ),
    )

    assert created.Id is not None
    # The association was created in the same call — the attribute is NOT orphaned.
    assocs = await _associations_for(session, created.Id)
    assert len(assocs) == 1
    assert assocs[0].EntityId == entity.Id


async def test_create_attribute_without_entity_id_makes_no_association(test_db_session):
    """Backward-compatible: no EntityId -> attribute only, no association (unchanged behaviour)."""
    session = test_db_session
    dm, entity = await _seed_model_and_entity(session, "noassoc")

    created = await create_attribute(
        session,
        CreateAttributeDTO(
            Name="size", UniqueName=f"{entity.UniqueName}.size", DataType="xsd:string", DataModelId=dm.Id
        ),
    )

    assert created.Id is not None
    assert await _associations_for(session, created.Id) == []
