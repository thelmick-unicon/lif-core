from typing import Dict, Optional

from fastapi import APIRouter, Depends, Query
from lif.mdr_services import search_service
from lif.mdr_utils.database_setup import get_session
from lif.mdr_utils.logger_config import get_logger
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=Dict[str, list])
async def search_data_model_api(
    data_model_id: Optional[int] = None,
    contributor_organization: Optional[str] = None,
    only_extension: Optional[bool] = False,
    only_base: Optional[bool] = False,
    search_key: str = Query(..., min_length=1),
    session: AsyncSession = Depends(get_session),
):
    results = await search_service.search_data_model(
        session,
        search_key=search_key,
        data_model_id=data_model_id,
        contributor_organization=contributor_organization,
        only_extension=only_extension,
        only_base=only_base,
    )
    return results
