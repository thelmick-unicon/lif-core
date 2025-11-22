import types
import pytest
from unittest.mock import AsyncMock, MagicMock

pytestmark = pytest.mark.asyncio

svc = pytest.importorskip("lif.mdr_services.datamodel_service")


class _ScalarListResult:
    """Mimic SA result where .scalars().all()/first() are used."""

    def __init__(self, items):
        self._items = list(items)

    def scalars(self):
        return self

    def all(self):
        return list(self._items)

    def first(self):
        return self._items[0] if self._items else None


class _CountResult:
    """Mimic SA result where .scalar() is used to get a count."""

    def __init__(self, n: int):
        self._n = n

    def scalar(self):
        return int(self._n)


@pytest.fixture
def fake_session():
    session = MagicMock()
    session.execute = AsyncMock()
    session.get = AsyncMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture(autouse=True)
def patch_dto_from_orm(monkeypatch):
    if hasattr(svc, "DataModelDTO"):
        dto_cls = getattr(svc, "DataModelDTO")
        monkeypatch.setattr(
            dto_cls,
            "from_orm",
            staticmethod(lambda obj: {"Id": getattr(obj, "Id", None), "Name": getattr(obj, "Name", None)}),
            raising=False,
        )


async def test_get_datamodel_by_id_ok(fake_session):
    dm = types.SimpleNamespace(Id=123, Name="Core", Deleted=False)
    fake_session.get.return_value = dm

    out = await svc.get_datamodel_by_id(fake_session, 123)
    assert out is dm
    fake_session.get.assert_awaited_once()


async def test_get_datamodel_by_id_not_found_raises(fake_session):
    fake_session.get.return_value = None
    with pytest.raises(svc.HTTPException) as exc:
        await svc.get_datamodel_by_id(fake_session, 999)
    assert exc.value.status_code == 404


async def test_get_datamodel_by_id_deleted_raises(fake_session):
    fake_session.get.return_value = types.SimpleNamespace(Id=5, Deleted=True)
    with pytest.raises(svc.HTTPException) as exc:
        await svc.get_datamodel_by_id(fake_session, 5)
    assert exc.value.status_code == 404


async def test_get_all_datamodels_returns_list(fake_session):
    fake_items = [
        types.SimpleNamespace(Id=1, Name="A", Deleted=False),
        types.SimpleNamespace(Id=2, Name="B", Deleted=False),
    ]
    fake_session.execute.return_value = _ScalarListResult(fake_items)

    out = await svc.get_all_datamodels(fake_session)
    assert isinstance(out, list)
    assert [o.Id for o in out] == [1, 2]
    fake_session.execute.assert_awaited_once()


async def test_get_paginated_datamodels_no_pagination(fake_session, monkeypatch):
    rows = [
        types.SimpleNamespace(Id=10, Name="X", Deleted=False),
        types.SimpleNamespace(Id=11, Name="Y", Deleted=False),
    ]
    fake_session.execute.side_effect = [_CountResult(2), _ScalarListResult(rows)]

    total_count, dtos = await svc.get_paginated_datamodels(
        fake_session, offset=0, limit=100, pagination=False, level_of_access=None, state=None, include_extension=True
    )

    assert total_count == 2
    assert isinstance(dtos, list)
    assert dtos == [{"Id": 10, "Name": "X"}, {"Id": 11, "Name": "Y"}]
    assert fake_session.execute.await_count == 2
