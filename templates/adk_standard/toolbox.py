import yfinance as yf
from duckduckgo_search import DDGS

def get_market_data(ticker: str):
    """Fetches real-time stock data for a given ticker."""
    data = yf.Ticker(ticker).info
    return {
        "price": data.get("regularMarketPrice"),
        "recommendation": data.get("recommendationKey"),
        "summary": data.get("longBusinessSummary")[:500]
    }

def web_search(query: str):
    """Performs a web search to find latest industry trends."""
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=3)]
    return results

# ADK Toolbox Mapping
GLOBAL_TOOLBOX = {
    "finance": [get_market_data],
    "general": [web_search],
    "research": [web_search, get_market_data]
}
