import os
import google.generativeai as genai
from datetime import datetime
from duckduckgo_search import DDGS

class CustomerServiceAgent:
    """Specialized ADK Agent for the Customer Service Industry."""
    
    def __init__(self, api_key, model_id="gemini-2.0-pro-exp-02-05"):
        genai.configure(api_key=api_key)
        self.model_id = model_id
        
        self.system_instruction = """
        You are the 'Service-ADK' Lead Concierge.
        Focus: Technical support, billing resolution, and high-fidelity customer interactions.
        
        PROTOCOLS:
        1. Empathy: Acknowledge customer frustrations and maintain a polite, helpful tone.
        2. Troubleshooting: Use a step-by-step approach to resolve technical issues.
        3. Escalation: Know when a problem requires a human supervisor and propose a seamless handoff.
        
        Current Time: {now}
        """.format(now=datetime.now())
        
        self.model = genai.GenerativeModel(
            model_name=self.model_id,
            tools=[self.search_support_kb],
            system_instruction=self.system_instruction
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def search_support_kb(self, issue: str):
        """Searches public knowledge bases for common troubleshooting steps and support articles."""
        with DDGS() as ddgs:
            return [r for r in ddgs.text(f"troubleshooting and support guide for {issue}", max_results=5)]

    def run(self, prompt):
        response = self.chat.send_message(prompt)
        return response.text

if __name__ == "__main__":
    key = os.getenv("GEMINI_API_KEY")
    if key:
        agent = CustomerServiceAgent(key)
        print(agent.run("How do I troubleshoot a connectivity issue with a 5G industrial router?"))
