from typing import Any, Dict

from fastapi import APIRouter, Depends, Query, Request, Response, status
from lif.mdr_dto.datamodel_constraints_dto import (
    CreateDataModelConstraintsDTO,
    DataModelConstraintsDTO,
    UpdateDataModelConstraintsDTO,
)
from lif.mdr_services import datamodel_constraints_service
from lif.mdr_utils.database_setup import get_session
from lif.mdr_utils.logger_config import get_logger
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
logger = get_logger(__name__)


# Create an entity association
@router.post("/", response_model=DataModelConstraintsDTO, status_code=status.HTTP_201_CREATED)
async def create_association(
    dto: CreateDataModelConstraintsDTO, response: Response, session: AsyncSession = Depends(get_session)
):
    # Call the service to create the entity association
    entity_association = await datamodel_constraints_service.create_data_model_constraint(session, dto)

    # Set the Location header with the new entity association ID
    response.headers["Location"] = f"/datamodel_constraints/{entity_association.Id}"

    return entity_association


# Get an entity association by ID
@router.get("/{constraint_id}", response_model=DataModelConstraintsDTO)
async def get_association(constraint_id: int, session: AsyncSession = Depends(get_session)):
    return await datamodel_constraints_service.get_data_model_constraint_by_id(session, constraint_id)


# Update an entity association by ID
@router.put("/{constraint_id}")
async def update_association(
    constraint_id: int, dto: UpdateDataModelConstraintsDTO, session: AsyncSession = Depends(get_session)
):
    return await datamodel_constraints_service.update_data_model_constraint(session, constraint_id, dto)


# Delete an entity association by ID
@router.delete("/{constraint_id}")
async def delete_association(constraint_id: int, session: AsyncSession = Depends(get_session)):
    return await datamodel_constraints_service.soft_delete_data_model_constraint(session, constraint_id)


@router.get("/", response_model=Dict[str, Any])
async def get_all_entity_association(
    request: Request,
    session: AsyncSession = Depends(get_session),
    page: int = Query(1, ge=1),  # Page number, default is 1
    size: int = Query(10, ge=1),  # Page size, default is 10
    pagination: bool = True,
):
    # Calculate offset
    offset = (page - 1) * size

    (total_count, constraints) = await datamodel_constraints_service.get_paginated_data_model_constraints(
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
            "data": constraints,
        }

    return {"total": total_count, "data": constraints}


@router.get("/by_data_model_id/{data_model_id}", response_model=Dict[str, Any])
async def get_entity_associations(
    data_model_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session),
    page: int = Query(1, ge=1),  # Page number, default is 1
    size: int = Query(10, ge=1),  # Page size, default is 10
    pagination: bool = True,
):
    # Calculate offset
    offset = (page - 1) * size

    (total_count, constraints) = await datamodel_constraints_service.get_data_model_constraints_by_data_model_id(
        session=session, data_model_id=data_model_id, offset=offset, limit=size, pagination=pagination
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
            "data": constraints,
        }

    return {"total": total_count, "data": constraints}
