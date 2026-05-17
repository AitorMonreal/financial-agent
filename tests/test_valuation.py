import unittest
from src.logic.valuation import (
    calculate_dcf, 
    run_monte_carlo_dcf, 
    calculate_industrial_deficit, 
    evaluate_precious_metal_regime
)

class TestValuation(unittest.TestCase):
    
    def test_calculate_dcf_standard(self):
        # Arrange
        base_fcf = 100.0
        growth = 0.10
        wacc = 0.08
        term_growth = 0.03
        
        # Act
        val = calculate_dcf(base_fcf, growth, wacc, term_growth, years=5)
        
        # Assert
        self.assertTrue(val > 0)
        self.assertAlmostEqual(val, 2786.41, places=2)

    def test_calculate_dcf_invalid_wacc(self):
        # WACC less than terminal growth should raise ValueError
        with self.assertRaisesRegex(ValueError, "WACC must be strictly greater"):
            calculate_dcf(100, 0.10, 0.02, 0.03)

    def test_monte_carlo_dcf(self):
        # Act
        res = run_monte_carlo_dcf(100.0, 0.10, 0.02, 0.08, 0.03, iterations=1000)
        
        # Assert
        self.assertIn("p5", res)
        self.assertIn("median", res)
        self.assertIn("p95", res)
        
        # p5 < median < p95 due to normal distribution of growth rates
        self.assertTrue(res["p5"] < res["median"] < res["p95"])

    def test_monte_carlo_dcf_invalid_std_dev(self):
        with self.assertRaises(ValueError):
            run_monte_carlo_dcf(100.0, 0.10, -0.02, 0.08, 0.03)

    def test_industrial_deficit(self):
        # Demand exceeds supply
        deficit = calculate_industrial_deficit(ev_demand=500, ess_demand=300, supply=700)
        self.assertEqual(deficit, 100)
        
        # Supply exceeds demand
        surplus = calculate_industrial_deficit(ev_demand=500, ess_demand=300, supply=900)
        self.assertEqual(surplus, -100)

    def test_precious_metal_regime(self):
        # High central bank and fiat debasement, low/negative real rate
        self.assertEqual(evaluate_precious_metal_regime(1.0, 1.0, 0.0), "Strong Accumulation")
        
        # Moderate factors
        self.assertEqual(evaluate_precious_metal_regime(0.5, 0.5, 0.5), "Moderate Accumulation")
        
        # Low factors, high real rate
        self.assertEqual(evaluate_precious_metal_regime(0.0, 0.0, 0.5), "Distribution")
