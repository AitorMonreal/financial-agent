import yfinance as yf
from typing import Dict, Any, Optional

class MarketDataClient:
    def __init__(self, fmp_api_key: Optional[str] = None):
        self.fmp_api_key = fmp_api_key

    def fetch_current_price(self, ticker: str) -> float:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1d")
        if history.empty:
            raise ValueError(f"No price data found for {ticker}")
        
        # Assuming the last close price
        # We use .iloc[-1] to get the last row's close value
        try:
            return float(history['Close'].iloc[-1])
        except Exception as e:
            raise ValueError(f"Failed to extract price for {ticker}: {e}")

    def fetch_fundamentals(self, ticker: str) -> Dict[str, Any]:
        """
        Fetches basic fundamentals via yfinance.
        If FMP key is provided, it could fetch deeper data as a fallback.
        """
        stock = yf.Ticker(ticker)
        info = stock.info
        
        fundamentals = {
            "market_cap": info.get("marketCap"),
            "forward_pe": info.get("forwardPE"),
            "trailing_pe": info.get("trailingPE"),
            "beta": info.get("beta"),
            "dividend_yield": info.get("dividendYield"),
            "sector": info.get("sector")
        }
        
        # Optional FMP fallback logic can be added here if fields are missing
        if self.fmp_api_key and fundamentals["sector"] is None:
            # Placeholder for FMP logic
            pass

        return fundamentals
