import os
import google.generativeai as genai
from datetime import datetime
from duckduckgo_search import DDGS

class LegalAgent:
    """Specialized ADK Agent for the Legal Industry."""
    
    def __init__(self, api_key, model_id="gemini-2.0-pro-exp-02-05"):
        genai.configure(api_key=api_key)
        self.model_id = model_id
        
        self.system_instruction = """
        You are the 'Legal-ADK' Counsel Assistant.
        Focus: Contract review, case law research, and regulatory compliance.
        
        PROTOCOLS:
        1. High Precision: Analyze documents for specific legal nuances, caveats, and red flags.
        2. Citations: If mentioning case law or statutes, provide citations where possible.
        3. Compliance: Align analysis with current regional laws (GDPR, California Consumer Privacy Act, etc.).
        
        Current Time: {now}
        """.format(now=datetime.now())
        
        self.model = genai.GenerativeModel(
            model_name=self.model_id,
            tools=[self.search_legal_precedents],
            system_instruction=self.system_instruction
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def search_legal_precedents(self, legal_query: str):
        """Web search for legal statutes, case laws, and legislative updates."""
        with DDGS() as ddgs:
            return [r for r in ddgs.text(f"legal precedent and statutes {legal_query}", max_results=5)]

    def run(self, prompt):
        response = self.chat.send_message(prompt)
        return response.text

if __name__ == "__main__":
    key = os.getenv("GEMINI_API_KEY")
    if key:
        agent = LegalAgent(key)
        print(agent.run("Provide a summary of recent changes to EU data privacy laws."))
