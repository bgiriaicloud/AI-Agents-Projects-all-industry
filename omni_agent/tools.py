import yfinance as yf
from duckduckgo_search import DDGS

def finance_tool(ticker: str):
    """Provides financial summary and live stock data for any company ticker."""
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "price": info.get("currentPrice"),
        "analyst_rating": info.get("recommendationKey"),
        "summary": info.get("longBusinessSummary", "")[:300]
    }

def healthcare_tool(query: str):
    """Scans medical knowledge bases for latest research and symptom insights (Educational use only)."""
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(f"high quality medical research {query}", max_results=3)]
    return results

def manufacturing_tool(equipment_id: str):
    """Simulates real-time IoT sensor data for factory equipment and predicts maintenance."""
    import random
    return {
        "equipment": equipment_id,
        "temperature": f"{random.randint(60, 95)}C",
        "vibration_level": "Normal" if random.random() > 0.2 else "High Warning",
        "recommendation": "Maintain Normal Operations" if random.random() > 0.1 else "Schedule Emergency Inspection"
    }

def research_tool(query: str):
    """Universal web search tool for trending news and industry shifts across all sectors."""
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=5)]
    return results

# Tool Mapping for ADK Hub
FULL_CAPABILITIES = [finance_tool, healthcare_tool, manufacturing_tool, research_tool]
