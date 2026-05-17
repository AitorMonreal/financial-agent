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
        self.base_url = "https://ndcdyn.interactivebrokers.com/AccountManagement/FlexWebService"

    def fetch_portfolio(self) -> List[PortfolioItem]:
        """
        Uses py-ibkr to fetch and parse the Flex Query.
        This isolates the integration so it can be mocked.
        """
        # We will import the actual py-ibkr library here.
        # Given we need a deterministic bridge without relying on unknown third-party internals,
        # we wrap it in our typed PortfolioItem.
        try:
            from ibkr import FlexClient
            client = FlexClient(token=self.token)
            report = client.get_report(query_id=self.query_id)
            
            items = []
            for position in report.open_positions:
                items.append(PortfolioItem(
                    symbol=position.symbol,
                    assetCategory=position.assetCategory,
                    position=position.position,
                    costBasisPrice=position.costBasisPrice,
                    currency=position.currency
                ))
            return items
        except ImportError:
            # Fallback for testing/mocking if py-ibkr module is named differently
            raise NotImplementedError("py-ibkr module structure not found or not mocked")
