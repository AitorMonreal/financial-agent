import os
from dotenv import load_dotenv

load_dotenv('.env.local')
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

from src.orchestration.graph import build_graph
from src.delivery.email_service import generate_html_report, send_email_report

def main():
    print("Initializing Satellite Portfolio AI Engine...")
    
    token = os.environ.get("IBKR_FLEX_TOKEN")
    query_id = os.environ.get("IBKR_FLEX_QUERY_ID")
    
    if not token or not query_id:
        print("Warning: Missing IBKR credentials. Simulating for dev purposes.")
        from src.connectors.ibkr_client import PortfolioItem
        portfolio = [
            PortfolioItem(symbol="AAPL", assetCategory="STK", position=10.0, costBasisPrice=120.0, currency="USD"),
            PortfolioItem(symbol="GC=F", assetCategory="CMDTY", position=1.0, costBasisPrice=2000.0, currency="USD")
        ]
    else:
        from src.connectors.ibkr_client import IBKRClient, PortfolioItem
        client = IBKRClient(token, query_id)
        try:
            portfolio = client.fetch_portfolio()
        except NotImplementedError:
            print("Warning: IBKR module missing. Simulating for dev purposes.")
            portfolio = [
                PortfolioItem(symbol="AAPL", assetCategory="STK", position=10.0, costBasisPrice=120.0, currency="USD"),
                PortfolioItem(symbol="GC=F", assetCategory="CMDTY", position=1.0, costBasisPrice=2000.0, currency="USD")
            ]
        
    print(f"Fetched {len(portfolio)} assets from portfolio.")
    
    app = build_graph()
    final_reports = []
    
    for asset in portfolio:
        print(f"Processing {asset.ticker}...")
        
        initial_state = {
            "asset": asset,
            "current_price": 0.0,
            "market_data": {},
            "historical_context": "",
            "equity_thesis": None,
            "macro_regime": None,
            "critic_feedback": None,
            "feedback_loop_count": 0,
            "intrinsic_value_distribution": None,
            "industrial_deficit": None,
            "precious_metal_regime": None,
            "final_summary": None
        }
        
        try:
            final_state = app.invoke(initial_state)
            
            dist = final_state.get("intrinsic_value_distribution")
            p50 = dist.get("median") if dist else None
            
            summary_obj = final_state.get("final_summary")
            summary_text = summary_obj.summary if summary_obj else "Summary generation failed."
            
            report_data = {
                "ticker": asset.ticker,
                "asset_class": asset.asset_class,
                "current_price": final_state.get("current_price", 0.0),
                "summary": summary_text,
                "intrinsic_median": p50,
                "regime": final_state.get("precious_metal_regime")
            }
            final_reports.append(report_data)
            print(f"Completed analysis for {asset.ticker}.")
            
        except Exception as e:
            print(f"Error processing {asset.ticker}: {e}")
            
    if final_reports:
        print("Generating HTML report...")
        html_content = generate_html_report(final_reports)
        
        with open("latest_report.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("Saved debug report to latest_report.html")
        
        try:
            print("Dispatching email...")
            send_email_report(html_content)
            print("Email dispatched successfully.")
        except ValueError as ve:
            print(f"Skipping email dispatch: {ve}")
        except Exception as e:
            print(f"Failed to send email: {e}")
    else:
        print("No reports generated.")

if __name__ == "__main__":
    main()
