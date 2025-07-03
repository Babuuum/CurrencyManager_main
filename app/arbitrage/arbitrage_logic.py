import os

from dotenv import load_dotenv

from app.exchanges.Kucoin_api import KuCoinAPI
from app.exchanges.Bybit_api import BybitAPI

load_dotenv()

api_key_kucoin = os.getenv('KUCOIN_API_KEY')
api_secret_kucoin = os.getenv('KUCOIN_API_SECRET')
passphrase_kucoin = os.getenv('KUCOIN_API_PASSWORD')

api_secret_bybit = os.getenv('BYBIT_API_SECRET')
api_key_bybit = os.getenv('BYBIT_API_KEY')

uniswap_secret = os.getenv('INFURA_API_KEY')


async def find_arbitrage_opportunity(symbol) -> dict | None:
    prices = {}
    try:
        kucoin_api = KuCoinAPI(api_key_kucoin, api_secret_kucoin, passphrase_kucoin)
        prices["kucoin"] = await kucoin_api.get_price(symbol)
    except Exception as e:
        prices["kucoin"] = None
        print(f"KuCoin error: {e}")

    try:
        bybit_api = BybitAPI(api_key_bybit, api_secret_bybit)
        prices["bybit"] = await bybit_api.get_price(symbol)
    except Exception as e:
        prices["bybit"] = None
        print(f"Bybit error: {e}")

    prices = {k: v for k, v in prices.items() if v is not None}
    if len(prices) < 2:
        print("Недостаточно данных для арбитража")
        return None

    min_ex = min(prices, key=prices.get)
    max_ex = max(prices, key=prices.get)
    min_price = prices[min_ex]
    max_price = prices[max_ex]
    spread = (max_price - min_price) / min_price * 100

    result = {
        "prices": prices,
        "buy_exchange": min_ex,
        "sell_exchange": max_ex,
        "spread_percent": spread,
        "is_opportunity": spread > 0.5
    }
    return result

async def arbitrage_get_pairs(exchanges_list: list, top_n=10) -> set:
    pairs = set()
    for exchange in exchanges_list:
        top_pairs = await exchange.liquid_pairs(top_n=top_n)
        pairs.update([symbol for symbol, _ in top_pairs])

    return pairs

async def arbitrage_main(kucoin: bool = True, bybit: bool = True, top_n=10):
    exchanges_list = []
    result = {}

    if kucoin:
        kucoin_api = KuCoinAPI(api_key_kucoin, api_secret_kucoin, passphrase_kucoin)
        exchanges_list.append(kucoin_api)

    if bybit:
        bybit_api = BybitAPI(api_key_bybit, api_secret_bybit)
        exchanges_list.append(bybit_api)

    if not exchanges_list:
        return None

    pairs = await arbitrage_get_pairs(exchanges_list, top_n=top_n)

    for pair in pairs:
        try:
            opportunity = await find_arbitrage_opportunity(pair)
        except Exception as e:
            print(f"Ошибка при проверке {pair}: {e}")
            continue

        if opportunity and opportunity['is_opportunity']:
            result[pair] = opportunity

    for ex in exchanges_list:
        await ex.exchange.close()

    return result

if __name__ == "__main__":
    qlist = ['BTC/USDT', 'ETH/USDT', 'LTC/USDT', 'SOL/USDT', 'XRP/USDT', 'ADA/USDT', 'BNB/USDT', 'DOGE/USDT', 'TRX/USDT', 'AVAX/USDT']
    [print(find_arbitrage_opportunity(i), "\n") for i in qlist]