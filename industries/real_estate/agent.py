import os
import google.generativeai as genai
from datetime import datetime
from duckduckgo_search import DDGS

class RealEstateAgent:
    """Specialized ADK Agent for the Real Estate Industry."""
    
    def __init__(self, api_key, model_id="gemini-2.0-pro-exp-02-05"):
        genai.configure(api_key=api_key)
        self.model_id = model_id
        
        self.system_instruction = """
        You are the 'RealEstate-ADK' Property Investment Advisor.
        Focus: Property valuation, market trend prediction, and lead nurturing.
        
        PROTOCOLS:
        1. Market Insight: Use real-time data to analyze neighborhood trends and pricing shifts.
        2. Investment ROI: Focus on Cap rates, cash-on-cash return, and potential appreciation.
        3. Compliance: Be aware of regional zoning laws and fair housing regulations.
        
        Current Time: {now}
        """.format(now=datetime.now())
        
        self.model = genai.GenerativeModel(
            model_name=self.model_id,
            tools=[self.search_real_estate_market],
            system_instruction=self.system_instruction
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def search_real_estate_market(self, location: str):
        """Web search for latest real estate market reports and pricing trends in a specific city/region."""
        with DDGS() as ddgs:
            return [r for r in ddgs.text(f"real estate market trends and property prices {location}", max_results=5)]

    def run(self, prompt):
        response = self.chat.send_message(prompt)
        return response.text

if __name__ == "__main__":
    key = os.getenv("GEMINI_API_KEY")
    if key:
        agent = RealEstateAgent(key)
        print(agent.run("Provide a market analysis for commercial real estate in Austin, Texas."))
