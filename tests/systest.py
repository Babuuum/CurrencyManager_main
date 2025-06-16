import pytest
import respx
from httpx import Response
from app.services.coingecko import get_price

@pytest.mark.asyncio
@respx.mock
async def test_get_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=Bitcoin&vs_currencies=usdt"
    respx.get(url).mock(return_value=Response(200, json={"Bitcoin": {"usdt": 42000.0}}))

    result = await get_price("BTC")

    assert result == 42000.0