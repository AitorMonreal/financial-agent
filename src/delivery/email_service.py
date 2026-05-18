import smtplib
from email.message import EmailMessage
import os
from jinja2 import Environment, FileSystemLoader

def generate_html_report(reports: list) -> str:
    """
    Renders the Jinja2 HTML report template.
    `reports` is a list of dicts with:
    - ticker
    - current_price
    - summary
    - asset_class
    - intrinsic_median (optional)
    - regime (optional)
    """
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('report.html')
    
    return template.render(reports=reports)

def send_email_report(html_content: str):
    """
    Dispatches the HTML email securely using smtplib.
    """
    sender = os.environ.get("SENDER_EMAIL")
    receiver = os.environ.get("RECEIVER_EMAIL")
    password = os.environ.get("GMAIL_APP_PASSWORD")
    
    if not all([sender, receiver, password]):
        raise ValueError("Missing email credentials in environment variables.")
        
    msg = EmailMessage()
    msg['Subject'] = "Weekly Satellite Portfolio AI Insights"
    msg['From'] = sender
    msg['To'] = receiver
    
    msg.set_content(html_content, subtype='html')
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)
