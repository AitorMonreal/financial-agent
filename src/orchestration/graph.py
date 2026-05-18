from langgraph.graph import StateGraph, END
from src.orchestration.state import AgentState
from src.connectors.market_data import MarketDataClient
from src.agents.analyst import run_equity_analysis, run_macro_analysis
from src.agents.critic import run_critic_review
from src.logic.valuation import run_monte_carlo_dcf, evaluate_precious_metal_regime
from src.agents.controller import generate_summary

# Instantiate shared clients
market_client = MarketDataClient()

def node_ingest_data(state: AgentState) -> AgentState:
    ticker = state["asset"].ticker
    state["current_price"] = market_client.fetch_current_price(ticker)
    state["market_data"] = market_client.fetch_fundamentals(ticker)
    state["historical_context"] = f"Recent earnings and transcripts for {ticker}."
    return state

def node_analyst(state: AgentState) -> AgentState:
    asset_class = state["asset"].asset_class
    
    if asset_class == "STK":
        state["equity_thesis"] = run_equity_analysis(state["historical_context"])
    else:
        state["macro_regime"] = run_macro_analysis(state["historical_context"])
        
    return state

def node_critic(state: AgentState) -> AgentState:
    asset_class = state["asset"].asset_class
    
    if asset_class == "STK" and state.get("equity_thesis"):
        feedback = run_critic_review(state["equity_thesis"], state["historical_context"])
        state["critic_feedback"] = feedback
        state["feedback_loop_count"] = state.get("feedback_loop_count", 0) + 1
    return state

def route_from_critic(state: AgentState) -> str:
    feedback = state.get("critic_feedback")
    
    if feedback is None or feedback.approved:
        return "node_valuation"
        
    loop_count = state.get("feedback_loop_count", 0)
    if loop_count >= 3:
        return "node_valuation"
        
    return "node_analyst"

def node_valuation(state: AgentState) -> AgentState:
    asset_class = state["asset"].asset_class
    
    if asset_class == "STK":
        fcf = 100.0
        wacc = 0.08
        term_growth = 0.03
        
        feedback = state.get("critic_feedback")
        sentiment = 0.0
        if feedback and not feedback.approved:
            sentiment = feedback.corrected_sentiment_score
        elif state.get("equity_thesis"):
            sentiment = state["equity_thesis"].sentiment_score
            
        mean_growth = 0.05 + sentiment
        dist = run_monte_carlo_dcf(fcf, mean_growth, 0.02, wacc, term_growth)
        state["intrinsic_value_distribution"] = dist
        
    elif asset_class == "CMDTY":
        macro = state.get("macro_regime")
        if macro:
            regime = evaluate_precious_metal_regime(
                macro.central_bank_demand_score,
                macro.fiat_debasement_score,
                0.02
            )
            state["precious_metal_regime"] = regime
            
    return state

def node_controller(state: AgentState) -> AgentState:
    ticker = state["asset"].ticker
    price = state.get("current_price", 0.0)
    dist = state.get("intrinsic_value_distribution", {})
    
    p50 = dist.get("median", 0.0) if dist else 0.0
    
    state["final_summary"] = generate_summary(ticker, p50, price)
    return state

def build_graph() -> StateGraph:
    workflow = StateGraph(AgentState)
    
    workflow.add_node("node_ingest_data", node_ingest_data)
    workflow.add_node("node_analyst", node_analyst)
    workflow.add_node("node_critic", node_critic)
    workflow.add_node("node_valuation", node_valuation)
    workflow.add_node("node_controller", node_controller)
    
    workflow.set_entry_point("node_ingest_data")
    workflow.add_edge("node_ingest_data", "node_analyst")
    workflow.add_edge("node_analyst", "node_critic")
    
    workflow.add_conditional_edges(
        "node_critic",
        route_from_critic,
        {
            "node_valuation": "node_valuation",
            "node_analyst": "node_analyst"
        }
    )
    
    workflow.add_edge("node_valuation", "node_controller")
    workflow.add_edge("node_controller", END)
    
    return workflow.compile()
