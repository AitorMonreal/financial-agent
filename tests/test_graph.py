import unittest
from unittest.mock import patch, MagicMock
from src.orchestration.state import AgentState
from src.connectors.ibkr_client import PortfolioItem
from src.agents.schemas import ThesisExtraction, CriticFeedback, SummaryReport
from src.orchestration.graph import build_graph

class TestLangGraphOrchestration(unittest.TestCase):

    @patch('src.orchestration.graph.market_client')
    @patch('src.orchestration.graph.run_equity_analysis')
    @patch('src.orchestration.graph.run_critic_review')
    @patch('src.orchestration.graph.run_monte_carlo_dcf')
    @patch('src.orchestration.graph.generate_summary')
    def test_full_equity_pipeline_approved(self, mock_summary, mock_mcf, mock_critic, mock_analyst, mock_market):
        # Arrange
        mock_market.fetch_current_price.return_value = 150.0
        mock_market.fetch_fundamentals.return_value = {"market_cap": 2000}
        
        mock_analyst.return_value = ThesisExtraction(sentiment_score=0.01, key_drivers=["a"])
        mock_critic.return_value = CriticFeedback(approved=True, reasoning="good", corrected_sentiment_score=0.0)
        
        mock_mcf.return_value = {"p5": 100.0, "median": 160.0, "p95": 200.0}
        mock_summary.return_value = SummaryReport(summary="Buy.")
        
        app = build_graph()
        
        initial_state: AgentState = {
            "asset": PortfolioItem(symbol="AAPL", assetCategory="STK", position=10.0, costBasisPrice=120.0, currency="USD"),
            "current_price": 0.0,
            "market_data": {},
            "historical_context": "",
            "equity_thesis": None,
            "macro_regime": None,
            "critic_feedback": None,
            "feedback_loop_count": 0,
            "intrinsic_value_distribution": None,
            "industrial_deficit": None,
            "precious_metal_regime": None,
            "final_summary": None
        }
        
        # Act
        final_state = app.invoke(initial_state)
        
        # Assert
        self.assertEqual(final_state["current_price"], 150.0)
        self.assertEqual(final_state["equity_thesis"].sentiment_score, 0.01)
        self.assertTrue(final_state["critic_feedback"].approved)
        self.assertEqual(final_state["intrinsic_value_distribution"]["median"], 160.0)
        self.assertEqual(final_state["final_summary"].summary, "Buy.")
        self.assertEqual(final_state["feedback_loop_count"], 1)

    @patch('src.orchestration.graph.market_client')
    @patch('src.orchestration.graph.run_equity_analysis')
    @patch('src.orchestration.graph.run_critic_review')
    @patch('src.orchestration.graph.run_monte_carlo_dcf')
    @patch('src.orchestration.graph.generate_summary')
    def test_full_equity_pipeline_rejected_feedback_loop(self, mock_summary, mock_mcf, mock_critic, mock_analyst, mock_market):
        # Arrange
        mock_market.fetch_current_price.return_value = 150.0
        mock_market.fetch_fundamentals.return_value = {}
        
        mock_analyst.return_value = ThesisExtraction(sentiment_score=0.05, key_drivers=["a"])
        # We will make critic reject it the first 3 times to hit loop max
        mock_critic.return_value = CriticFeedback(approved=False, reasoning="too high", corrected_sentiment_score=0.01)
        
        mock_mcf.return_value = {"median": 160.0}
        mock_summary.return_value = SummaryReport(summary="Hold.")
        
        app = build_graph()
        
        initial_state: AgentState = {
            "asset": PortfolioItem(symbol="AAPL", assetCategory="STK", position=10.0, costBasisPrice=120.0, currency="USD"),
            "current_price": 0.0,
            "market_data": {},
            "historical_context": "",
            "equity_thesis": None,
            "macro_regime": None,
            "critic_feedback": None,
            "feedback_loop_count": 0,
            "intrinsic_value_distribution": None,
            "industrial_deficit": None,
            "precious_metal_regime": None,
            "final_summary": None
        }
        
        # Act
        final_state = app.invoke(initial_state)
        
        # Assert
        self.assertFalse(final_state["critic_feedback"].approved)
        # Should loop exactly 3 times before breaking to valuation
        self.assertEqual(final_state["feedback_loop_count"], 3)
