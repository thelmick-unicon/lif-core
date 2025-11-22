from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Query, Request, Response, status
from lif.mdr_dto.value_set_values_dto import CreateValueSetValueDTO, UpdateValueSetValueDTO, ValueSetValueDTO
from lif.mdr_services import value_set_values_service
from lif.mdr_utils.database_setup import get_session
from lif.mdr_utils.logger_config import get_logger
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=Dict[str, Any])
async def get_value_set_values(
    request: Request,
    session: AsyncSession = Depends(get_session),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    pagination: bool = True,
):
    # Calculate offset
    offset = (page - 1) * size

    (total_count, value_set_values) = await value_set_values_service.get_paginated_value_set_values(
        session, offset, size, pagination
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
            "data": value_set_values,
        }

    return {"total": total_count, "data": value_set_values}


@router.get("/{id}", response_model=ValueSetValueDTO)
async def get_value_set_value(id: int, session: AsyncSession = Depends(get_session)):
    return await value_set_values_service.get_value_set_value_by_id(session, id)


@router.post("/", response_model=List[ValueSetValueDTO], status_code=status.HTTP_201_CREATED)
async def create_value_set_values(
    data: List[CreateValueSetValueDTO], response: Response, session: AsyncSession = Depends(get_session)
):
    values = await value_set_values_service.create_value_set_values(session, data)
    # Set the Location header with the new entity association ID
    # response.headers["Location"] = f"/value_set_values/{value.Id}"
    return values


@router.put("/{id}", response_model=ValueSetValueDTO)
async def update_value_set_value(id: int, data: UpdateValueSetValueDTO, session: AsyncSession = Depends(get_session)):
    return await value_set_values_service.update_value_set_value(session, id, data)


@router.delete("/{id}")
async def delete_value_set_value(id: int, session: AsyncSession = Depends(get_session)):
    return await value_set_values_service.soft_delete_value_set_value(session, id)


@router.get("/by_valueset_id/{valueset_id}", response_model=Dict[str, Any])
async def get_value_set_values_for_a_value_set(
    request: Request,
    valueset_id: int,
    session: AsyncSession = Depends(get_session),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    pagination: bool = True,
):
    # Calculate offset
    offset = (page - 1) * size

    (total_count, value_set_values) = await value_set_values_service.get_list_of_values_for_value_set(
        session, valueset_id, offset, size, pagination=pagination
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
            "data": value_set_values,
        }

    return {"total": total_count, "data": value_set_values}
