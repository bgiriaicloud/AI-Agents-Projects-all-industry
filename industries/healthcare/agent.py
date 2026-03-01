import os
import google.generativeai as genai
from datetime import datetime
from duckduckgo_search import DDGS

class HealthcareAgent:
    """Specialized ADK Agent for the Healthcare Industry."""
    
    def __init__(self, api_key, model_id="gemini-2.0-pro-exp-02-05"):
        genai.configure(api_key=api_key)
        self.model_id = model_id
        
        self.system_instruction = """
        You are the 'Healthcare-ADK' Specialist. 
        Focus: Medical report analysis, health insights, and clinical trial matching.
        
        PROTOCOLS:
        1. Accuracy: Prioritize medical research and verified sources.
        2. Safety: Always state you are an AI, not a doctor. Never provide prescriptions.
        3. Terminology: Use professional medical terminology but explain it simply for patients.
        4. Data Privacy: Remind users not to share sensitive PII (Personally Identifiable Information).
        
        Current Time: {now}
        """.format(now=datetime.now())
        
        self.model = genai.GenerativeModel(
            model_name=self.model_id,
            tools=[self.search_medical_updates],
            system_instruction=self.system_instruction
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def search_medical_updates(self, query: str):
        """Web search for the latest medical research and healthcare trends."""
        with DDGS() as ddgs:
            return [r for r in ddgs.text(f"medical research {query}", max_results=5)]

    def run(self, prompt):
        response = self.chat.send_message(prompt)
        return response.text

if __name__ == "__main__":
    # Example Usage
    key = os.getenv("GEMINI_API_KEY") 
    agent = HealthcareAgent(key)
    print(agent.run("What are the latest advancements in personalized cancer treatment?"))
