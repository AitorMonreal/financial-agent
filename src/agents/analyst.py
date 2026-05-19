from pydantic_ai import Agent
import os
from src.agents.schemas import ThesisExtraction, MacroRegimeExtraction

AGENT_MODEL = os.environ.get('AGENT_MODEL', 'gemini-2.5-flash')

equity_analyst_agent = Agent(
    AGENT_MODEL,
    output_type=ThesisExtraction,
    system_prompt=(
        "You are an expert equity analyst. Read the provided fundamental text and extract a qualitative sentiment score "
        "between -0.05 and +0.05 to shift the mean of a DCF Monte Carlo simulation. Be extremely conservative."
    )
)

macro_analyst_agent = Agent(
    AGENT_MODEL,
    output_type=MacroRegimeExtraction,
    system_prompt=(
        "You are an expert macro-economist. Read the provided market news and extract scores for central bank demand "
        "and fiat debasement risk."
    )
)

def run_equity_analysis(text_context: str) -> ThesisExtraction:
    result = equity_analyst_agent.run_sync(f"Analyze this: {text_context}")
    return result.output

def run_macro_analysis(text_context: str) -> MacroRegimeExtraction:
    result = macro_analyst_agent.run_sync(f"Analyze this: {text_context}")
    return result.output
