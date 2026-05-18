from typing import TypedDict, Optional, Dict, Any
from src.connectors.ibkr_client import PortfolioItem
from src.agents.schemas import ThesisExtraction, MacroRegimeExtraction, CriticFeedback, SummaryReport

class AgentState(TypedDict):
    # Data Layer
    asset: PortfolioItem
    current_price: float
    market_data: Dict[str, Any]
    historical_context: str
    
    # Analysis Layer
    equity_thesis: Optional[ThesisExtraction]
    macro_regime: Optional[MacroRegimeExtraction]
    
    # Feedback Layer
    critic_feedback: Optional[CriticFeedback]
    feedback_loop_count: int
    
    # Core Math Layer
    intrinsic_value_distribution: Optional[Dict[str, float]]
    industrial_deficit: Optional[float]
    precious_metal_regime: Optional[str]
    
    # Delivery Layer
    final_summary: Optional[SummaryReport]
