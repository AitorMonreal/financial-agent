import numpy as np
from typing import Dict

def calculate_dcf(free_cash_flow: float, growth_rate: float, wacc: float, terminal_growth_rate: float, years: int = 5) -> float:
    """
    Calculates the intrinsic value using a parameterized Discounted Cash Flow model.
    """
    if wacc <= terminal_growth_rate:
        raise ValueError("WACC must be strictly greater than terminal growth rate to calculate terminal value.")
    
    present_value = 0.0
    projected_fcf = free_cash_flow

    for year in range(1, years + 1):
        projected_fcf *= (1 + growth_rate)
        present_value += projected_fcf / ((1 + wacc) ** year)

    terminal_value = (projected_fcf * (1 + terminal_growth_rate)) / (wacc - terminal_growth_rate)
    present_terminal_value = terminal_value / ((1 + wacc) ** years)

    return present_value + present_terminal_value

def run_monte_carlo_dcf(
    base_fcf: float, 
    mean_growth_rate: float, 
    std_dev_growth: float, 
    wacc: float, 
    terminal_growth_rate: float, 
    iterations: int = 10000
) -> Dict[str, float]:
    """
    Runs a Monte Carlo simulation around the DCF growth rate to produce a probabilistic distribution.
    Returns the 5th, 50th (median), and 95th percentiles of intrinsic value.
    """
    if std_dev_growth < 0:
        raise ValueError("Standard deviation must be non-negative.")

    # Set seed for reproducible deterministic tests. In production, this can be parameterized.
    np.random.seed(42)
    simulated_growth_rates = np.random.normal(loc=mean_growth_rate, scale=std_dev_growth, size=iterations)

    intrinsic_values = []
    for g in simulated_growth_rates:
        try:
            val = calculate_dcf(base_fcf, g, wacc, terminal_growth_rate)
            intrinsic_values.append(val)
        except ValueError:
            continue

    if not intrinsic_values:
        raise ValueError("All Monte Carlo iterations resulted in invalid DCF calculations.")

    return {
        "p5": float(np.percentile(intrinsic_values, 5)),
        "median": float(np.median(intrinsic_values)),
        "p95": float(np.percentile(intrinsic_values, 95))
    }

def calculate_industrial_deficit(ev_demand: float, ess_demand: float, supply: float) -> float:
    """
    Calculates the structural deficit for industrial metals.
    Positive value indicates a deficit (demand > supply).
    Negative value indicates a surplus.
    """
    total_demand = ev_demand + ess_demand
    return total_demand - supply

def evaluate_precious_metal_regime(
    central_bank_demand_score: float, 
    fiat_debasement_score: float, 
    real_interest_rate: float
) -> str:
    """
    Maps macro sentiment scores (0 to 1) and real interest rates to a qualitative accumulation regime.
    """
    aggregate_score = (central_bank_demand_score * 0.4) + (fiat_debasement_score * 0.4) - (real_interest_rate * 0.2)
    
    if aggregate_score >= 0.6:
        return "Strong Accumulation"
    elif aggregate_score >= 0.3:
        return "Moderate Accumulation"
    elif aggregate_score >= 0.0:
        return "Neutral"
    else:
        return "Distribution"
