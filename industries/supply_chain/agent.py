import os
import google.generativeai as genai
from datetime import datetime
from duckduckgo_search import DDGS

class SupplyChainAgent:
    """Specialized ADK Agent for the Supply Chain Industry."""
    
    def __init__(self, api_key, model_id="gemini-2.0-pro-exp-02-05"):
        genai.configure(api_key=api_key)
        self.model_id = model_id
        
        self.system_instruction = """
        You are the 'SupplyChain-ADK' Logistics Orchestrator.
        Focus: Route optimization, inventory forecasting, and vendor negotiation.
        
        PROTOCOLS:
        1. Resilience: Always propose contingency plans for port strikes, weather delays, or geopolitical shifts.
        2. Efficiency: Focus on reducing 'lead time' and 'deadweight' in the logistical loop.
        3. Real-time Visibility: Use tools to check global shipping and freight status.
        
        Current Time: {now}
        """.format(now=datetime.now())
        
        self.model = genai.GenerativeModel(
            model_name=self.model_id,
            tools=[self.search_shipping_alerts],
            system_instruction=self.system_instruction
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def search_shipping_alerts(self, route: str):
        """Web search for latest port congestion, shipping delays, and logistical alerts on major trade routes."""
        with DDGS() as ddgs:
            return [r for r in ddgs.text(f"global shipping and logistics delays {route}", max_results=5)]

    def run(self, prompt):
        response = self.chat.send_message(prompt)
        return response.text

if __name__ == "__main__":
    key = os.getenv("GEMINI_API_KEY")
    if key:
        agent = SupplyChainAgent(key)
        print(agent.run("What are the current logistical bottlenecks in the Suez Canal?"))
