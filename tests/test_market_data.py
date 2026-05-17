import unittest
from unittest.mock import patch, MagicMock
from src.connectors.market_data import MarketDataClient
import pandas as pd

class TestMarketDataClient(unittest.TestCase):
    def setUp(self):
        self.client = MarketDataClient(fmp_api_key="fake_key")

    @patch('src.connectors.market_data.yf.Ticker')
    def test_fetch_current_price_success(self, mock_ticker_class):
        # Arrange
        mock_ticker = MagicMock()
        mock_ticker_class.return_value = mock_ticker
        
        # Create a dummy DataFrame to simulate yfinance history
        data = {'Close': [150.0]}
        mock_df = pd.DataFrame(data)
        mock_ticker.history.return_value = mock_df

        # Act
        price = self.client.fetch_current_price("AAPL")

        # Assert
        self.assertEqual(price, 150.0)
        mock_ticker.history.assert_called_once_with(period="1d")

    @patch('src.connectors.market_data.yf.Ticker')
    def test_fetch_current_price_empty_history(self, mock_ticker_class):
        # Arrange
        mock_ticker = MagicMock()
        mock_ticker_class.return_value = mock_ticker
        
        mock_df = pd.DataFrame() # empty
        mock_ticker.history.return_value = mock_df

        # Act & Assert
        with self.assertRaisesRegex(ValueError, "No price data found for AAPL"):
            self.client.fetch_current_price("AAPL")

    @patch('src.connectors.market_data.yf.Ticker')
    def test_fetch_fundamentals(self, mock_ticker_class):
        # Arrange
        mock_ticker = MagicMock()
        mock_ticker_class.return_value = mock_ticker
        
        mock_ticker.info = {
            "marketCap": 2000000000,
            "forwardPE": 25.5,
            "trailingPE": 26.0,
            "beta": 1.2,
            "dividendYield": 0.015,
            "sector": "Technology"
        }

        # Act
        fundamentals = self.client.fetch_fundamentals("AAPL")

        # Assert
        self.assertEqual(fundamentals["market_cap"], 2000000000)
        self.assertEqual(fundamentals["sector"], "Technology")
        self.assertEqual(fundamentals["beta"], 1.2)
