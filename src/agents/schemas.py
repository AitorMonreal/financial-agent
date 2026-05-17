from pydantic import BaseModel, Field
from typing import List

class ThesisExtraction(BaseModel):
    sentiment_score: float = Field(
        description="A score between -0.05 and 0.05 representing the qualitative shift in growth based on text.",
        ge=-0.05,
        le=0.05
    )
    key_drivers: List[str] = Field(description="Top 3 key drivers identified in the text.")

class MacroRegimeExtraction(BaseModel):
    central_bank_demand_score: float = Field(description="Score between 0 and 1 indicating central bank accumulation.", ge=0, le=1)
    fiat_debasement_score: float = Field(description="Score between 0 and 1 indicating fiat debasement risk.", ge=0, le=1)

class CriticFeedback(BaseModel):
    approved: bool = Field(description="True if the thesis is mathematically sound and conservative.")
    reasoning: str = Field(description="Explanation of approval or rejection.")
    corrected_sentiment_score: float = Field(
        description="If rejected, the suggested corrected sentiment score.",
        ge=-0.05,
        le=0.05,
        default=0.0
    )

class SummaryReport(BaseModel):
    summary: str = Field(description="A concise two-sentence summary of the asset's current state and outlook.")
