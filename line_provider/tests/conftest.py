import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from line_provider.main import service, app  

@pytest.fixture(scope="function")
def reset_repository():
    service.repo._events.clear()
    print(service.repo._events)
    yield
    service.repo._events.clear()

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
