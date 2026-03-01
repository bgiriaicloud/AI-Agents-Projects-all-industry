import os
import google.generativeai as genai
from datetime import datetime
import yfinance as yf

class FinanceAgent:
    """Specialized ADK Agent for the Financial Industry."""
    
    def __init__(self, api_key, model_id="gemini-2.0-pro-exp-02-05"):
        genai.configure(api_key=api_key)
        self.model_id = model_id
        
        self.system_instruction = """
        You are the 'Finance-ADK' Specialist.
        Focus: Stock market analysis, equity research, and risk management.
        
        PROTOCOLS:
        1. Quantitative Focus: Prioritize hard data, percentages, and financial metrics.
        2. Market Awareness: Use tools to get real-time price and analyst sentiment.
        3. Risk Disclosure: Always mention that financial decisions carry risk and past performance is not indicative of future results.
        
        Current Time: {now}
        """.format(now=datetime.now())
        
        self.model = genai.GenerativeModel(
            model_name=self.model_id,
            tools=[self.get_stock_info],
            system_instruction=self.system_instruction
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def get_stock_info(self, ticker: str):
        """Fetches real-time financial data, analyst recommendations, and company info for a ticker."""
        stock = yf.Ticker(ticker)
        return stock.info

    def run(self, prompt):
        response = self.chat.send_message(prompt)
        return response.text

if __name__ == "__main__":
    key = os.getenv("GEMINI_API_KEY")
    if key:
        agent = FinanceAgent(key)
        print(agent.run("Provide an analysis of Nvidia's (NVDA) current market position."))
