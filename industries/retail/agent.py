import os
import google.generativeai as genai
from datetime import datetime
from duckduckgo_search import DDGS

class RetailAgent:
    """Specialized ADK Agent for Retail & E-commerce."""
    
    def __init__(self, api_key, model_id="gemini-2.0-pro-exp-02-05"):
        genai.configure(api_key=api_key)
        self.model_id = model_id
        
        self.system_instruction = """
        You are the 'Retail-ADK' Merchandising Expert.
        Focus: Inventory optimization, trend analysis, and personalized customer stylists.
        
        PROTOCOLS:
        1. Customer-Centric: Focus on CX (Customer Experience) and personalization.
        2. Trends: Use tools to check latest fashion and consumer tech trends.
        3. Operational efficiency: Recommend markdown strategies for slow-moving stock.
        
        Current Time: {now}
        """.format(now=datetime.now())
        
        self.model = genai.GenerativeModel(
            model_name=self.model_id,
            tools=[self.search_retail_trends],
            system_instruction=self.system_instruction
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def search_retail_trends(self, category: str):
        """Web search for latest retail trends and competitor pricing in a given category."""
        with DDGS() as ddgs:
            return [r for r in ddgs.text(f"retail and ecommerce trends 2026 {category}", max_results=5)]

    def run(self, prompt):
        response = self.chat.send_message(prompt)
        return response.text

if __name__ == "__main__":
    key = os.getenv("GEMINI_API_KEY")
    if key:
        agent = RetailAgent(key)
        print(agent.run("What are the predicted fashion trends for Summer 2026?"))
