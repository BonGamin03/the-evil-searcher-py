import json
import requests
from typing import Any
from domain.i_web_searcher import IWebSearcher

class ZenserpSearcher(IWebSearcher):
    """Implementation of IWebSearcher using the Zenserp API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://app.zenserp.com/api/v2/search"

    def search(self, query: str) -> list[Any]:
        headers = {
            "apikey": self.api_key
        }
        params = (
            ("q", query),
            ("tbm", "nws"),
            ("hl", "es"),
        )
        print(self.api_key)
        response = requests.get(self.url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        
         

        # Zenserp news search results are typically under 'news_results'
        return data.get("news_results", [])
    