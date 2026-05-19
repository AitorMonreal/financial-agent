from pydantic_ai import Agent
import os
from src.agents.schemas import SummaryReport

AGENT_MODEL = os.environ.get('AGENT_MODEL', 'gemini-2.5-flash')

controller_agent = Agent(
    AGENT_MODEL,
    output_type=SummaryReport,
    system_prompt=(
        "You are a portfolio controller. Synthesize the final deterministic numerical outputs into a concise 2-sentence summary."
    )
)

def generate_summary(asset_name: str, intrinsic_value_p50: float, current_price: float) -> SummaryReport:
    prompt = f"Asset: {asset_name}. Median Intrinsic Value: {intrinsic_value_p50}. Current Price: {current_price}."
    result = controller_agent.run_sync(prompt)
    return result.output
