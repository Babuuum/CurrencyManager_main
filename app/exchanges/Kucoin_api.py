import ccxt.async_support as ccxt

class KuCoinAPI:
    def __init__(self, api_key, api_secret, passphrase):
        self.exchange = ccxt.kucoin({
            'apiKey': api_key,
            'secret': api_secret,
            'password': passphrase,
        })

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.exchange.close()

    async def get_price(self, symbol):
        ticker = await self.exchange.fetch_ticker(symbol)
        return ticker['last']

    async def liquid_pairs(self, top_n=50, quote='USDT'):
        await self.exchange.load_markets()
        tickers = await self.exchange.fetch_tickers()
        pairs_with_vol = []
        for symbol, ticker in tickers.items():
            if quote and not symbol.endswith(f"/{quote}"):
                continue

            volume = ticker.get('quoteVolume') or ticker.get('baseVolume') or 0
            if volume > 0:
                pairs_with_vol.append((symbol, volume))
        pairs_with_vol.sort(key=lambda x: x[1], reverse=True)
        return pairs_with_vol[:top_n]