from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Query, Request, Response, status
from lif.mdr_dto.attribute_dto import AttributeDTO, CreateAttributeDTO, UpdateAttributeDTO
from lif.mdr_services import attribute_service, tag_service
from lif.mdr_utils.database_setup import get_session
from lif.mdr_utils.logger_config import get_logger
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=Dict[str, Any])
async def get_attributes(
    request: Request,
    session: AsyncSession = Depends(get_session),
    page: int = Query(1, ge=1),  # Page number, default is 1
    size: int = Query(10, ge=1),  # Page size, default is 10
    pagination: bool = True,
):
    # Calculate offset
    offset = (page - 1) * size

    total_count, attributes = await attribute_service.get_paginated_attributes(
        session=session, offset=offset, limit=size, pagination=pagination
    )

    if pagination:
        total_pages = (total_count + size - 1) // size
        base_url = str(request.url).split("?")[0]
        next_url = f"{base_url}?page={page + 1}&size={size}" if page < total_pages else None
        previous_url = f"{base_url}?page={page - 1}&size={size}" if page > 1 else None

        return {
            "total": total_count,
            "page": page,
            "size": size,
            "total_pages": total_pages,
            "next": next_url,
            "previous": previous_url,
            "data": attributes,
        }

    return {"total": total_count, "data": attributes}


@router.get("/{attribute_id}", response_model=AttributeDTO)
async def get_attribute_by_id(attribute_id: int, session: AsyncSession = Depends(get_session)):
    attribute = await attribute_service.get_attribute_dto_by_id(session, attribute_id)
    return attribute


@router.post("/", response_model=AttributeDTO, status_code=status.HTTP_201_CREATED)
async def create_attribute(data: CreateAttributeDTO, response: Response, session: AsyncSession = Depends(get_session)):
    attribute = await attribute_service.create_attribute(session, data)
    # Set the Location header
    response.headers["Location"] = f"/attributes/{attribute.Id}"
    return attribute


@router.put("/{attribute_id}", response_model=AttributeDTO)
async def update_attribute(attribute_id: int, data: UpdateAttributeDTO, session: AsyncSession = Depends(get_session)):
    return await attribute_service.update_attribute(session, attribute_id, data)


@router.delete("/{attribute_id}")
async def delete_attribute(attribute_id: int, session: AsyncSession = Depends(get_session)):
    return await attribute_service.soft_delete_attribute(session, attribute_id)


@router.get("/attributes/by_ids/", response_model=List[AttributeDTO])
async def get_attributes_by_ids(
    ids: List[int] = Query(...),  # List of attribute IDs to fetch
    session: AsyncSession = Depends(get_session),
):
    return await attribute_service.get_attributes_by_ids(session, ids)


@router.get("/by_entity_id/{entity_id}", response_model=Dict[str, Any])
async def get_attributes_for_entity(
    request: Request,
    entity_id: int,
    data_model_id: int = 1,  # Default to 1 (BaseLIF)
    session: AsyncSession = Depends(get_session),
    page: int = Query(1, ge=1),  # Page number, default is 1
    size: int = Query(10, ge=1),  # Page size, default is 10
    pagination: bool = True,
):
    # Calculate offset
    offset = (page - 1) * size

    total_count, attributes = await attribute_service.get_list_of_attributes_for_entity(
        session=session,
        entity_id=entity_id,
        data_model_id=data_model_id,
        offset=offset,
        limit=size,
        pagination=pagination,
    )

    if pagination:
        total_pages = (total_count + size - 1) // size
        base_url = str(request.url).split("?")[0]
        next_url = f"{base_url}?page={page + 1}&size={size}" if page < total_pages else None
        previous_url = f"{base_url}?page={page - 1}&size={size}" if page > 1 else None

        return {
            "total": total_count,
            "page": page,
            "size": size,
            "total_pages": total_pages,
            "next": next_url,
            "previous": previous_url,
            "data": attributes,
        }

    return {"total": total_count, "data": attributes}


@router.get("/by_data_model_id/{data_model_id}", response_model=Dict[str, Any])
async def get_attributes_by_data_model(
    request: Request,
    data_model_id: int,
    session: AsyncSession = Depends(get_session),
    page: int = Query(1, ge=1),  # Page number, default is 1
    size: int = Query(10, ge=1),  # Page size, default is 10
    pagination: bool = True,
    check_base: bool = True,
):
    # Calculate offset
    offset = (page - 1) * size

    (total_count, attributes) = await attribute_service.get_list_of_attributes_for_data_model(
        session=session,
        data_model_id=data_model_id,
        offset=offset,
        limit=size,
        pagination=pagination,
        check_base=check_base,
    )

    if pagination:
        total_pages = (total_count + size - 1) // size
        base_url = str(request.url).split("?")[0]
        next_url = f"{base_url}?page={page + 1}&size={size}" if page < total_pages else None
        previous_url = f"{base_url}?page={page - 1}&size={size}" if page > 1 else None

        return {
            "total": total_count,
            "page": page,
            "size": size,
            "total_pages": total_pages,
            "next": next_url,
            "previous": previous_url,
            "data": attributes,
        }

    return {"total": total_count, "data": attributes}


@router.post("/tags/{attribute_id}", status_code=status.HTTP_201_CREATED)
async def add_tags_for_attribute(
    attribute_id: int, tags: List[str] = Query(...), session: AsyncSession = Depends(get_session)
):
    return await tag_service.add_tags(
        session=session, id=attribute_id, tags=tags, element_type=tag_service.TagElementType.Attribute
    )


@router.delete("/tags/{attribute_id}")
async def delete_tags_for_attribute(
    attribute_id: int, tags: List[str] = Query(...), session: AsyncSession = Depends(get_session)
):
    return await tag_service.delete_tags(
        session=session, id=attribute_id, tags=tags, element_type=tag_service.TagElementType.Attribute
    )


@router.get("/tags/{attribute_id}")
async def get_tags_for_attribute(attribute_id: int, session: AsyncSession = Depends(get_session)):
    return await tag_service.get_tags(
        session=session, id=attribute_id, element_type=tag_service.TagElementType.Attribute
    )
