from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Query, Request, Response, status
from lif.mdr_dto.valueset_dto import CreateValueSetDTO, CreateValueSetWithValuesDTO, UpdateValueSetDTO, ValueSetDTO
from lif.mdr_services import tag_service, valueset_service
from lif.mdr_utils.database_setup import get_session
from lif.mdr_utils.logger_config import get_logger
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=Dict[str, Any])
async def get_value_sets(
    request: Request,
    session: AsyncSession = Depends(get_session),
    page: int = Query(1, ge=1),  # Page number, default is 1
    size: int = Query(10, ge=1),  # Page size, default is 10
    pagination: bool = True,
):
    # Calculate offset
    offset = (page - 1) * size

    # Call the service to get paginated value sets
    total_count, value_sets = await valueset_service.get_paginated_value_sets(
        session=session, offset=offset, limit=size, pagination=pagination
    )

    if pagination:
        # Calculate total pages
        total_pages = (total_count + size - 1) // size
        base_url = str(request.url).split("?")[0]
        next_url = f"{base_url}?page={page + 1}&size={size}" if page < total_pages else None
        previous_url = f"{base_url}?page={page - 1}&size={size}" if page > 1 else None

        # Return paginated results and metadata
        return {
            "total": total_count,
            "page": page,
            "size": size,
            "total_pages": total_pages,
            "next": next_url,
            "previous": previous_url,
            "data": value_sets,
        }

    return {"total": total_count, "data": value_sets}


@router.get("/{value_set_id}", response_model=ValueSetDTO)
async def get_value_set(value_set_id: int, session: AsyncSession = Depends(get_session)):
    # Fetch a single value set by ID
    value_set = await valueset_service.get_value_set_by_id(session, value_set_id)
    return value_set


@router.post("/", response_model=ValueSetDTO, status_code=status.HTTP_201_CREATED)
async def create_value_set(data: CreateValueSetDTO, response: Response, session: AsyncSession = Depends(get_session)):
    # Create a new value set
    value_set = await valueset_service.create_value_set(session, data)
    # Set the Location header with the new entity association ID
    response.headers["Location"] = f"/value_sets/{value_set.Id}"
    return value_set


@router.put("/{value_set_id}", response_model=ValueSetDTO)
async def update_value_set(value_set_id: int, data: UpdateValueSetDTO, session: AsyncSession = Depends(get_session)):
    # Update an existing value set
    return await valueset_service.update_value_set(session, value_set_id, data)


@router.delete("/{value_set_id}")
async def delete_value_set(value_set_id: int, session: AsyncSession = Depends(get_session)):
    # Delete a value set
    return await valueset_service.soft_delete_value_set(session, value_set_id)


@router.get("/by_ids/", response_model=List[ValueSetDTO])
async def get_valuesets_by_ids(
    ids: List[int] = Query(...),  # List of ValueSet IDs to fetch
    session: AsyncSession = Depends(get_session),
):
    return await valueset_service.get_valuesets_by_ids(session, ids)


# @router.get("/{value_set_id}/values", response_model=ValueSetAndValuesDTO)
# async def get_value_set(value_set_id: int, session: AsyncSession = Depends(get_session)):
#     # Fetch a single value set by ID
#     value_set = await valueset_service.get_list_of_values(session, value_set_id)
#     return value_set


@router.post("/with_values", response_model=ValueSetDTO)
async def create_value_set_with_value(data: CreateValueSetWithValuesDTO, session: AsyncSession = Depends(get_session)):
    # Create a new value set
    return await valueset_service.create_value_set_with_values(session, data)


@router.get("/by_data_model_id/{data_model_id}", response_model=Dict[str, Any])
async def get_value_sets_for_data_model(
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

    # Call the service to get paginated value sets
    (total_count, value_sets) = await valueset_service.get_paginated_value_sets_by_data_model_id(
        session=session, data_model_id=data_model_id, offset=offset, limit=size, pagination=pagination
    )

    if pagination:
        # Calculate total pages
        total_pages = (total_count + size - 1) // size
        base_url = str(request.url).split("?")[0]
        next_url = f"{base_url}?page={page + 1}&size={size}" if page < total_pages else None
        previous_url = f"{base_url}?page={page - 1}&size={size}" if page > 1 else None

        # Return paginated results and metadata
        return {
            "total": total_count,
            "page": page,
            "size": size,
            "total_pages": total_pages,
            "next": next_url,
            "previous": previous_url,
            "data": value_sets,
        }

    return {"total": total_count, "data": value_sets}


@router.get("/usage/{value_set_id}")
async def get_value_set(value_set_id: int, session: AsyncSession = Depends(get_session)):
    # Fetch a single value set by ID
    value_set = await valueset_service.get_attributes_by_value_set_id(session, value_set_id=value_set_id)
    return value_set


@router.post("/tags/{value_set_id}", status_code=status.HTTP_201_CREATED)
async def add_tags_for_value_set(
    value_set_id: int, tags: List[str] = Query(...), session: AsyncSession = Depends(get_session)
):
    return await tag_service.add_tags(
        session=session, id=value_set_id, tags=tags, element_type=tag_service.TagElementType.ValueSet
    )


@router.delete("/tags/{value_set_id}")
async def delete_tags_for_value_set(
    value_set_id: int, tags: List[str] = Query(...), session: AsyncSession = Depends(get_session)
):
    return await tag_service.delete_tags(
        session=session, id=value_set_id, tags=tags, element_type=tag_service.TagElementType.ValueSet
    )


@router.get("/tags/{value_set_id}")
async def get_tags_for_value_set(value_set_id: int, session: AsyncSession = Depends(get_session)):
    return await tag_service.get_tags(
        session=session, id=value_set_id, element_type=tag_service.TagElementType.ValueSet
    )
