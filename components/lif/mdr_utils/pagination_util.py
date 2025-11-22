from lif.mdr_utils.logger_config import get_logger

logger = get_logger(__name__)


def do_pagination(data, page_num: int, page_size: int, endpoint: str):
    response = {"data": data, "count": len(data), "pagination": {}}
    if page_num == 1:
        response["pagination"]["previous"] = None
    else:
        response["pagination"]["previous"] = f"/{endpoint}?page_num={page_num - 1}&page_size={page_size}"

    if len(data) < page_size:
        response["pagination"]["next"] = None
    else:
        response["pagination"]["next"] = f"/{endpoint}?page_num={page_num + 1}&page_size={page_size}"
    return response
