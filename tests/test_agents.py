import unittest
from unittest.mock import patch, MagicMock
from src.agents.schemas import ThesisExtraction, MacroRegimeExtraction, CriticFeedback, SummaryReport
from src.agents.analyst import run_equity_analysis, run_macro_analysis
from src.agents.critic import run_critic_review
from src.agents.controller import generate_summary

class TestAgents(unittest.TestCase):
    
    @patch('src.agents.analyst.equity_analyst_agent.run_sync')
    def test_run_equity_analysis(self, mock_run_sync):
        # Arrange
        mock_result = MagicMock()
        mock_result.output = ThesisExtraction(sentiment_score=0.01, key_drivers=["Revenue growth"])
        mock_run_sync.return_value = mock_result
        
        # Act
        extraction = run_equity_analysis("Positive earnings call transcript.")
        
        # Assert
        self.assertEqual(extraction.sentiment_score, 0.01)
        self.assertEqual(extraction.key_drivers[0], "Revenue growth")

    @patch('src.agents.analyst.macro_analyst_agent.run_sync')
    def test_run_macro_analysis(self, mock_run_sync):
        # Arrange
        mock_result = MagicMock()
        mock_result.output = MacroRegimeExtraction(central_bank_demand_score=0.8, fiat_debasement_score=0.7)
        mock_run_sync.return_value = mock_result
        
        # Act
        extraction = run_macro_analysis("Central banks buying gold.")
        
        # Assert
        self.assertEqual(extraction.central_bank_demand_score, 0.8)
        self.assertEqual(extraction.fiat_debasement_score, 0.7)

    @patch('src.agents.critic.critic_agent.run_sync')
    def test_run_critic_review_approved(self, mock_run_sync):
        # Arrange
        mock_result = MagicMock()
        mock_result.output = CriticFeedback(approved=True, reasoning="Conservative enough.", corrected_sentiment_score=0.0)
        mock_run_sync.return_value = mock_result
        
        analyst_output = ThesisExtraction(sentiment_score=0.01, key_drivers=["x"])
        
        # Act
        feedback = run_critic_review(analyst_output, "historical data")
        
        # Assert
        self.assertTrue(feedback.approved)
        self.assertEqual(feedback.corrected_sentiment_score, 0.0)

    @patch('src.agents.controller.controller_agent.run_sync')
    def test_generate_summary(self, mock_run_sync):
        # Arrange
        mock_result = MagicMock()
        mock_result.output = SummaryReport(summary="AAPL is undervalued. Hold.")
        mock_run_sync.return_value = mock_result
        
        # Act
        report = generate_summary("AAPL", 150.0, 140.0)
        
        # Assert
        self.assertEqual(report.summary, "AAPL is undervalued. Hold.")
