from pydantic_ai import Agent
import os
from src.agents.schemas import CriticFeedback, ThesisExtraction

AGENT_MODEL = os.environ.get('AGENT_MODEL', 'gemini-2.5-flash')

critic_agent = Agent(
    AGENT_MODEL,
    output_type=CriticFeedback,
    system_prompt=(
        "You are a strict, adversarial risk manager. Review the analyst's extraction. "
        "If the sentiment score is overly optimistic (>0.02) without strong evidence, reject it and provide a corrected score. "
        "Otherwise, approve."
    )
)

def run_critic_review(analyst_output: ThesisExtraction, historical_context: str) -> CriticFeedback:
    prompt = f"Analyst proposed score: {analyst_output.sentiment_score}. Historical context: {historical_context}. Review and approve or reject."
    result = critic_agent.run_sync(prompt)
    return result.output
