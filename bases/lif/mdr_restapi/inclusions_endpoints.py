from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Query, Request, Response, status
from lif.mdr_dto.inclusion_dto import CreateInclusionDTO, InclusionDTO, UpdateInclusionDTO
from lif.mdr_services import inclusions_service
from lif.mdr_utils.database_setup import get_session
from lif.mdr_utils.logger_config import get_logger
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
logger = get_logger(__name__)


@router.get("/{inclusion_id}", response_model=InclusionDTO)
async def get_inclusion(inclusion_id: int, session: AsyncSession = Depends(get_session)):
    inclusion = await inclusions_service.get_inclusion_by_id(session, inclusion_id)
    return inclusion


@router.post("/", response_model=InclusionDTO, status_code=status.HTTP_201_CREATED)
async def create_inclusion(data: CreateInclusionDTO, response: Response, session: AsyncSession = Depends(get_session)):
    inclusion = await inclusions_service.create_inclusion(session, data)
    # Set the Location header with the new inclusion association ID
    response.headers["Location"] = f"/inclusions/{inclusion.Id}"
    return inclusion


@router.put("/{inclusion_id}", response_model=InclusionDTO)
async def update_inclusion(inclusion_id: int, data: UpdateInclusionDTO, session: AsyncSession = Depends(get_session)):
    inclusion = await inclusions_service.update_inclusion(session, inclusion_id, data)
    return inclusion


@router.delete("/{inclusion_id}")
async def delete_inclusion(inclusion_id: int, session: AsyncSession = Depends(get_session)):
    return await inclusions_service.soft_delete_inclusion(session, inclusion_id)


@router.get("/by_data_model_id/{data_model_id}", response_model=Dict[str, Any])
async def get_inclusions_for_data_model(
    request: Request,
    data_model_id: int,
    session: AsyncSession = Depends(get_session),
    page: int = Query(1, ge=1),  # Default to page 1
    size: int = Query(10, ge=1),  # Default to 10 items per page
    pagination: bool = True,
    check_base: bool = True,
):
    # Calculate offset
    offset = (page - 1) * size

    # Call the service function to get total count and paginated results
    (total_count, inclusions) = await inclusions_service.get_list_of_inclusions_for_data_model(
        session, data_model_id, offset, size, pagination=pagination, check_base=check_base
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
            "data": inclusions,
        }

    return {"total": total_count, "data": inclusions}


@router.get("/entities/by_data_model_id/{data_model_id}", response_model=List[InclusionDTO])
async def get_entities_by_data_model_id(data_model_id: int, session: AsyncSession = Depends(get_session)):
    return await inclusions_service.get_entity_inclusions_by_data_model_id(session, data_model_id)


@router.get("/attributes/by_data_model_id/{data_model_id}", response_model=List[InclusionDTO])
async def get_attributes_by_data_model_id(data_model_id: int, session: AsyncSession = Depends(get_session)):
    return await inclusions_service.get_attribute_inclusions_by_data_model_id(session, data_model_id)


@router.get("/attributes/by_data_model_id/{data_model_id}/by_entity_id/{entity_id}", response_model=List[InclusionDTO])
async def get_attributes_by_data_model_id_and_entity_id(
    data_model_id: int, entity_id: int, session: AsyncSession = Depends(get_session)
):
    return await inclusions_service.get_attribute_inclusions_by_data_model_id_and_entity_id(
        session, data_model_id, entity_id
    )
