import unittest
from unittest.mock import patch, MagicMock
from src.connectors.ibkr_client import IBKRClient, PortfolioItem

class TestIBKRClient(unittest.TestCase):
    def setUp(self):
        self.client = IBKRClient(token="fake_token", query_id="fake_query_id")

    @patch('src.connectors.ibkr_client.IBKRClient.fetch_portfolio')
    def test_fetch_portfolio_returns_parsed_items(self, mock_fetch):
        # Arrange
        mock_fetch.return_value = [
            PortfolioItem(symbol="AAPL", assetCategory="STK", position=10.0, costBasisPrice=150.0, currency="USD"),
            PortfolioItem(symbol="GC=F", assetCategory="CMDTY", position=1.0, costBasisPrice=2000.0, currency="USD")
        ]

        # Act
        result = self.client.fetch_portfolio()

        # Assert
        self.assertEqual(len(result), 2)
        
        # Test Behavior: ensure mapping works
        aapl = result[0]
        self.assertEqual(aapl.ticker, "AAPL")
        self.assertEqual(aapl.asset_class, "STK")
        self.assertEqual(aapl.quantity, 10.0)
        
        gold = result[1]
        self.assertEqual(gold.ticker, "GC=F")
        self.assertEqual(gold.asset_class, "CMDTY")

    def test_initialization(self):
        # Arrange & Act
        client = IBKRClient(token="test1", query_id="test2")
        
        # Assert
        self.assertEqual(client.token, "test1")
        self.assertEqual(client.query_id, "test2")
