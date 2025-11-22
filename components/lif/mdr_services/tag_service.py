from enum import Enum
from typing import List
from fastapi import HTTPException
from lif.mdr_services.attribute_service import get_attribute_dto_by_id
from lif.mdr_services.datamodel_service import get_datamodel_by_id
from lif.mdr_services.entity_service import get_entity_by_id
from lif.mdr_services.transformation_service import get_transformation_group_by_id
from lif.mdr_services.valueset_service import get_value_set_by_id
from lif.mdr_utils.logger_config import get_logger
from sqlalchemy.ext.asyncio import AsyncSession


logger = get_logger(__name__)


class TagElementType(str, Enum):
    DataModel = "DataModel"
    Entity = "Entity"
    ValueSet = "ValueSet"
    TransformationGroup = "TransformationGroup"
    Attribute = "Attribute"


async def get_obj(session: AsyncSession, id: int, element_type: TagElementType):
    if element_type == TagElementType.DataModel:
        obj = await get_datamodel_by_id(session=session, id=id)
    elif element_type == TagElementType.Entity:
        obj = await get_entity_by_id(session=session, id=id)
    elif element_type == TagElementType.Attribute:
        obj = await get_attribute_dto_by_id(session=session, id=id)
    elif element_type == TagElementType.ValueSet:
        obj = await get_value_set_by_id(session=session, id=id)
    elif element_type == TagElementType.TransformationGroup:
        obj = await get_transformation_group_by_id(session=session, id=id)
    else:
        raise HTTPException(status_code=400, detail="Not supported element type.")
    return obj


async def add_tags(session: AsyncSession, id: int, tags: List[str], element_type: TagElementType):
    obj = await get_obj(session=session, id=id, element_type=element_type)
    obj.Tags += "," + ",".join(tags)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return {"ok": True}


async def delete_tags(session: AsyncSession, id: int, tags: list[str], element_type: TagElementType):
    obj = await get_obj(session=session, id=id, element_type=element_type)
    obj_tags_set = set(obj.Tags.split(","))
    tags_set = set(tags)
    final_set = obj_tags_set - tags_set
    obj.Tags = ",".join(final_set)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return {"ok": True}


async def get_tags(session: AsyncSession, id: int, element_type: TagElementType):
    obj = await get_obj(session=session, id=id, element_type=element_type)
    return obj.Tags.split(",")
