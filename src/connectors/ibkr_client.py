import os
import requests
from typing import List, Dict, Any
from pydantic import BaseModel, Field

class PortfolioItem(BaseModel):
    ticker: str = Field(alias="symbol")
    asset_class: str = Field(alias="assetCategory")
    quantity: float = Field(alias="position")
    cost_basis: float = Field(alias="costBasisPrice")
    currency: str

class IBKRClient:
    def __init__(self, token: str, query_id: str):
        self.token = token
        self.query_id = query_id
        self.base_url = "https://ndcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService"

    def fetch_portfolio(self) -> List[PortfolioItem]:
        """
        Uses native HTTP requests to fetch and parse the Flex Query CSV.
        """
        import time
        import csv
        import io
        import os
        import xml.etree.ElementTree as ET

        cache_file = ".ibkr_cache.csv"
        csv_data = None

        send_url = f"{self.base_url}.SendRequest?t={self.token}&q={self.query_id}&v=3"
        
        response = None
        for _ in range(5):
            response = requests.get(send_url)
            response.raise_for_status()
            if "Statement could not be generated" in response.text:
                time.sleep(5)
                continue
            break
            
        if "Success" in response.text:
            root = ET.fromstring(response.text)
            ref_code = root.find("ReferenceCode").text
            get_url = root.find("Url").text
            
            # Poll for the report
            poll_url = f"{get_url}?q={ref_code}&t={self.token}&v=3"
            
            for _ in range(10): # 10 attempts
                time.sleep(3) # Wait for report generation
                r2 = requests.get(poll_url)
                r2.raise_for_status()
                
                if "Statement in progress" in r2.text:
                    continue
                    
                csv_data = r2.text
                
                # Update the local cache with the fresh successful data
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write(csv_data)
                break

        # Fallback to local cache if IBKR aggressively rate limits us (ErrorCode 1001)
        if not csv_data and os.path.exists(cache_file):
            print("Notice: IBKR Flex Query rate-limited (ErrorCode 1001). Falling back to local cache.")
            with open(cache_file, "r", encoding="utf-8") as f:
                csv_data = f.read()
                
        if not csv_data:
            raise RuntimeError(f"IBKR Flex Query Failed: {response.text}")
            
        # Define a list of known commodity ETFs/Trusts that IBKR classifies as STK
        # but should be evaluated using macro/commodity logic rather than DCF.
        COMMODITY_ETFS = {"GLDM", "PSLV", "COPX", "URA"}
        
        items = []
        reader = csv.DictReader(io.StringIO(csv_data))
        for row in reader:
            # Skip summary rows or empty rows if any
            if not row.get("Symbol"):
                continue
                
            symbol = row["Symbol"]
            asset_class = "CMDTY" if symbol in COMMODITY_ETFS else row["AssetClass"]
                
            items.append(PortfolioItem(
                symbol=symbol,
                assetCategory=asset_class,
                position=float(row["Quantity"]),
                costBasisPrice=float(row["CostBasisPrice"]),
                currency=row["CurrencyPrimary"]
            ))
            
        return items
