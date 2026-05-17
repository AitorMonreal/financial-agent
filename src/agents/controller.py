from pydantic_ai import Agent
from src.agents.schemas import SummaryReport

controller_agent = Agent(
    'gemini-1.5-pro',
    result_type=SummaryReport,
    system_prompt=(
        "You are a portfolio controller. Synthesize the final deterministic numerical outputs into a concise 2-sentence summary."
    )
)

def generate_summary(asset_name: str, intrinsic_value_p50: float, current_price: float) -> SummaryReport:
    prompt = f"Asset: {asset_name}. Median Intrinsic Value: {intrinsic_value_p50}. Current Price: {current_price}."
    result = controller_agent.run_sync(prompt)
    return result.data
