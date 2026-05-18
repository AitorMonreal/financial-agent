# Setup Guide: Satellite Portfolio AI Engine

This document provides instructions on how to configure your local environment, install dependencies, and configure the necessary API keys to run the Satellite Portfolio AI Engine.

## Prerequisites

Before starting, ensure you have the following installed on your system:
*   **Python 3.10 or higher**: Required for Pydantic and LangGraph compatibility.
*   **Interactive Brokers Account**: You must have access to the Client Portal to configure Flex Queries.
*   **Gmail Account**: Required to dispatch the final weekly report.

## 1. Installation

It is highly recommended to run this project inside a Python virtual environment to avoid dependency conflicts.

1.  **Open your terminal** and navigate to the project root directory (`c:\src\finance-agent`).
2.  **Create a virtual environment:**
    ```powershell
    python -m venv .venv
    ```
3.  **Activate the virtual environment:**
    ```powershell
    # On Windows (PowerShell)
    .\.venv\Scripts\Activate.ps1
    
    # On macOS/Linux
    source .venv/bin/activate
    ```
4.  **Install the dependencies:**
    ```powershell
    pip install -r requirements.txt
    ```

## 2. Environment Variables

The project uses `python-dotenv` to load secrets from a `.env` file. We have provided a `.env.example` file in the repository.

1.  Copy `.env.example` to a new file named `.env`:
    ```powershell
    cp .env.example .env
    ```
2.  Open `.env` and fill in the required values:

### Obtaining the Variables:

*   **`IBKR_FLEX_TOKEN` & `IBKR_FLEX_QUERY_ID`**:
    1. Log in to the Interactive Brokers Client Portal.
    2. Go to **Performance & Reports > Flex Queries**.
    3. Click the gear icon next to "Flex Web Service" to generate a Token.
    4. Create a new "Portfolio Report" query. Ensure it includes Ticker, Position, Cost Basis, and Currency. Save it and note the generated **Query ID**.

*   **`FMP_API_KEY`** (Optional but recommended):
    1. Sign up for a free tier account at [Financial Modeling Prep](https://site.financialmodelingprep.com/).
    2. Retrieve your API key from the dashboard. This acts as a fallback for deep U.S. equity fundamentals.

*   **`GEMINI_API_KEY`**:
    1. Go to [Google AI Studio](https://aistudio.google.com/).
    2. Sign in and create a new API Key. This will power the Analyst, Critic, and Controller agents.

*   **`GMAIL_APP_PASSWORD`**:
    1. Go to your Google Account > Security.
    2. Ensure 2-Step Verification is turned on.
    3. Search for "App Passwords".
    4. Generate a new password (select "Other" and name it "Finance Agent"). Use this 16-character string in your `.env` file. Do *not* use your regular Gmail password.

*   **`SENDER_EMAIL` & `RECEIVER_EMAIL`**: 
    1. Enter the email addresses for routing the weekly HTML report. Usually, these are both your personal email address.

## 3. Running the Tests

The project adheres strictly to Test-Driven Development (TDD). Before deploying, ensure all core logic operates deterministically by running the test suite.

From the root directory, with your virtual environment activated, run:
```powershell
$env:PYTHONPATH="."
pytest tests/
```

## 4. Running the Engine

*Note: The orchestrator script is currently in development under Phase 5.*

Once finalized, the engine will be executed via a single entry point:
```powershell
python main.py
```
This script is designed to be completely headless and should ideally be scheduled to run autonomously using a tool like Windows Task Scheduler or a Unix `cron` job (e.g., scheduled for every Friday at 5:00 PM).
