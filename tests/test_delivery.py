import unittest
from unittest.mock import patch, MagicMock
from src.delivery.email_service import generate_html_report, send_email_report

class TestEmailService(unittest.TestCase):
    def test_generate_html_report(self):
        # Arrange
        reports = [
            {
                "ticker": "AAPL",
                "asset_class": "STK",
                "current_price": 150.0,
                "summary": "Undervalued.",
                "intrinsic_median": 160.0,
                "regime": None
            }
        ]
        
        # Act
        html_content = generate_html_report(reports)
        
        # Assert
        self.assertIn("AAPL", html_content)
        self.assertIn("150.00", html_content)
        self.assertIn("Undervalued.", html_content)
        self.assertIn("160.00", html_content)
        self.assertIn("Satellite Portfolio Insights", html_content)

    @patch('src.delivery.email_service.os.environ.get')
    @patch('src.delivery.email_service.smtplib.SMTP_SSL')
    def test_send_email_report_success(self, mock_smtp, mock_env):
        # Arrange
        def env_side_effect(key):
            if key == "SENDER_EMAIL": return "sender@gmail.com"
            if key == "RECEIVER_EMAIL": return "receiver@gmail.com"
            if key == "GMAIL_APP_PASSWORD": return "secret"
            return None
        mock_env.side_effect = env_side_effect
        
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Act
        send_email_report("<html>test</html>")
        
        # Assert
        mock_server.login.assert_called_once_with("sender@gmail.com", "secret")
        mock_server.send_message.assert_called_once()
        
    @patch('src.delivery.email_service.os.environ.get')
    def test_send_email_report_missing_credentials(self, mock_env):
        # Arrange
        mock_env.return_value = None
        
        # Act & Assert
        with self.assertRaises(ValueError):
            send_email_report("<html>test</html>")
