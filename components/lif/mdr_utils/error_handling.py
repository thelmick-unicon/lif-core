from http import HTTPStatus
from typing import Optional
from uuid import uuid4

from fastapi import HTTPException


def generate_unique_error_id() -> str:
    """
    Generates a UUID to use as an error id
    """
    return str(uuid4())


def generate_or_use_unique_error_id(error_id: Optional[str]) -> str:
    """
    Generates a UUID to use as an error id if one is not provided
    """
    if error_id is None:
        return generate_unique_error_id()
    return error_id


def log_error_template() -> str:
    """
    Simple log error format
    """
    return "ERROR_ID=[%s] - %s"


def build_exception(error_id: str, message: str, status_code: Optional[HTTPStatus]) -> HTTPException:
    """
    Provides guidance on structure and consistency for logging / handling errors.
    """
    status, headers, detail_message = build_exception_details(error_id, status_code, message)

    return HTTPException(status_code=status, detail=detail_message, headers=headers)


def build_exception_details(
    error_id: str, status_code: Optional[HTTPStatus], message: str
) -> tuple[HTTPStatus, dict[str, str], str]:
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR if status_code is None else status_code
    headers = {"error_id": error_id}
    return (status_code, headers, f"{message} Error ID: {error_id}")
