from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Query, Request, Response, status
from lif.mdr_dto.entity_dto import CreateEntityDTO, EntityDTO, UpdateEntityDTO
from lif.mdr_services import entity_service, tag_service
from lif.mdr_utils.database_setup import get_session
from lif.mdr_utils.logger_config import get_logger
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=Dict[str, Any])
async def get_entities(
    request: Request,
    session: AsyncSession = Depends(get_session),
    page: int = Query(1, ge=1),  # Default to page 1
    size: int = Query(10, ge=1),  # Default to 10 items per page
    pagination: bool = True,
):
    # Calculate offset
    offset = (page - 1) * size

    # Call the service function to get total count and paginated results
    total_count, entities = await entity_service.get_paginated_entities(session, offset, size, pagination)

    if pagination:
        # Calculate total pages
        total_pages = (total_count + size - 1) // size

        # Generate next and previous links
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
            "data": entities,
        }

    return {"total": total_count, "data": entities}


@router.get("/{entity_id}", response_model=EntityDTO)
async def get_entity(entity_id: int, session: AsyncSession = Depends(get_session)):
    entity = await entity_service.get_entity_by_id(session, entity_id)
    return entity


@router.get("/parents/{entity_id}", response_model=List[EntityDTO])
async def get_entity(entity_id: int, session: AsyncSession = Depends(get_session)):
    entities = await entity_service.get_entity_parents(session, entity_id)
    return entities


@router.get("/children/{entity_id}", response_model=List[EntityDTO])
async def get_entity(entity_id: int, session: AsyncSession = Depends(get_session)):
    entities = await entity_service.get_entity_children(session, entity_id)
    return entities


@router.get("/by_attribute_id/{attribute_id}", response_model=EntityDTO)
async def get_entity_by_attribute_id(attribute_id: int, session: AsyncSession = Depends(get_session)):
    entity = await entity_service.get_entity_by_attribute_id(session, attribute_id)
    return entity


@router.post("/", response_model=EntityDTO, status_code=status.HTTP_201_CREATED)
async def create_entity(data: CreateEntityDTO, response: Response, session: AsyncSession = Depends(get_session)):
    entity = await entity_service.create_entity(session, data)
    # Set the Location header with the new entity association ID
    response.headers["Location"] = f"/entities/{entity.Id}"
    return entity


@router.put("/{entity_id}", response_model=EntityDTO)
async def update_entity(entity_id: int, data: UpdateEntityDTO, session: AsyncSession = Depends(get_session)):
    entity = await entity_service.update_entity(session, entity_id, data)
    return entity


@router.delete("/{entity_id}")
async def delete_entity(entity_id: int, session: AsyncSession = Depends(get_session)):
    return await entity_service.soft_delete_entity(session, entity_id)


# @router.get("/{entity_id}/attributes/", response_model=EntityAttributeDTO)
# async def get_attributes_for_entity(id: int, session: AsyncSession = Depends(get_session)):
#     entity_attributes = await entity_service.get_list_of_attribute(session, id)
#     return entity_attributes


@router.get("/entities/by_ids/", response_model=List[EntityDTO])
async def get_entities_by_ids(
    ids: List[int] = Query(...),  # List of Entity IDs to fetch
    session: AsyncSession = Depends(get_session),
):
    return await entity_service.get_entities_by_ids(session, ids)


@router.get("/by_data_model_id/{data_model_id}", response_model=Dict[str, Any])
async def get_entities_for_data_model(
    request: Request,
    data_model_id: int,
    session: AsyncSession = Depends(get_session),
    page: int = Query(1, ge=1),  # Default to page 1
    size: int = Query(10, ge=1),  # Default to 10 items per page
    pagination: bool = True,
):
    # Calculate offset
    offset = (page - 1) * size

    # Call the service function to get total count and paginated results
    total_count, entities = await entity_service.get_list_of_entities_for_data_model(
        session, data_model_id, offset, size, pagination=pagination
    )

    if pagination:
        # Calculate total pages
        total_pages = (total_count + size - 1) // size

        # Generate next and previous links
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
            "data": entities,
        }

    return {"total": total_count, "data": entities}


@router.post("/tags/{entity_id}", status_code=status.HTTP_201_CREATED)
async def add_tags_for_entity(
    entity_id: int, tags: List[str] = Query(...), session: AsyncSession = Depends(get_session)
):
    return await tag_service.add_tags(
        session=session, id=entity_id, tags=tags, element_type=tag_service.TagElementType.Entity
    )


@router.delete("/tags/{entity_id}")
async def delete_tags_for_entity(
    entity_id: int, tags: List[str] = Query(...), session: AsyncSession = Depends(get_session)
):
    return await tag_service.delete_tags(
        session=session, id=entity_id, tags=tags, element_type=tag_service.TagElementType.Entity
    )


@router.get("/tags/{entity_id}")
async def get_tags_for_entity(entity_id: int, session: AsyncSession = Depends(get_session)):
    return await tag_service.get_tags(session=session, id=entity_id, element_type=tag_service.TagElementType.Entity)
