import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import AsyncMock, patch

from lif.translator_restapi import core


def get_client() -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=core.app), base_url="http://test")


def test_sample():
    assert core is not None


@pytest.mark.asyncio
async def test_translate_success():
    mock_translator_instance = AsyncMock()
    mock_translator_instance.run.return_value = {"translated": "data"}
    with patch("lif.translator_restapi.core.Translator", return_value=mock_translator_instance):
        async with get_client() as ac:
            response = await ac.post("/translate/source/source_schema/target/target_schema", json={"input": "data"})
    assert response.status_code == 200
    assert response.json() == {"translated": "data"}


@pytest.mark.asyncio
async def test_translate_schema_not_found():
    mock_translator_instance = AsyncMock()
    mock_translator_instance.run.side_effect = core.ResourceNotFoundException("invalid_source", "Schema not found")
    with patch("lif.translator_restapi.core.Translator", return_value=mock_translator_instance):
        async with get_client() as ac:
            response = await ac.post("/translate/source/invalid_source/target/invalid_target", json={"input": "data"})
    assert response.status_code == 404
    assert response.json()["message"] == "Schema not found"


@pytest.mark.asyncio
async def test_translate_value_error():
    mock_translator_instance = AsyncMock()
    mock_translator_instance.run.side_effect = ValueError("Data does not conform to schema: blah")
    with patch("lif.translator_restapi.core.Translator", return_value=mock_translator_instance):
        async with get_client() as ac:
            response = await ac.post("/translate/source/source_id/target/target_id", json={"input": "data"})
    assert response.status_code == 400
    assert response.json()["message"] == "Data does not conform to schema: blah"
