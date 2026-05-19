import unittest
from unittest.mock import patch, MagicMock
from src.connectors.ibkr_client import IBKRClient, PortfolioItem

class TestIBKRClient(unittest.TestCase):
    def setUp(self):
        self.client = IBKRClient(token="fake_token", query_id="fake_query_id")

    @patch('src.connectors.ibkr_client.requests.get')
    def test_fetch_portfolio_returns_parsed_items(self, mock_get):
        # Arrange
        mock_send_response = MagicMock()
        mock_send_response.text = '''<FlexStatementResponse>
            <Status>Success</Status>
            <ReferenceCode>12345</ReferenceCode>
            <Url>https://test.interactivebrokers.com</Url>
        </FlexStatementResponse>'''
        
        mock_poll_response = MagicMock()
        mock_poll_response.text = '''ClientAccountID,Symbol,Description,Quantity,MarkPrice,CostBasisPrice,CostBasisMoney,PositionValue,FifoPnlUnrealized,PercentOfNAV,AssetClass,CurrencyPrimary,ISIN,CUSIP
U123,AAPL,Apple Inc,10,150,120,1200,1500,300,10,STK,USD,,
U123,GC=F,Gold,1,2000,1800,1800,2000,200,5,CMDTY,USD,,'''
        
        mock_get.side_effect = [mock_send_response, mock_poll_response]

        # Act
        with patch('time.sleep', return_value=None):
            result = self.client.fetch_portfolio()

        # Assert
        self.assertEqual(len(result), 2)
        
        # Test Behavior: ensure mapping works
        aapl = result[0]
        self.assertEqual(aapl.ticker, "AAPL")
        self.assertEqual(aapl.asset_class, "STK")
        self.assertEqual(aapl.quantity, 10.0)
        self.assertEqual(aapl.cost_basis, 120.0)
        
        gold = result[1]
        self.assertEqual(gold.ticker, "GC=F")
        self.assertEqual(gold.asset_class, "CMDTY")

    def test_initialization(self):
        # Arrange & Act
        client = IBKRClient(token="test1", query_id="test2")
        
        # Assert
        self.assertEqual(client.token, "test1")
        self.assertEqual(client.query_id, "test2")
