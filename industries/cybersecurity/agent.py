import os
import google.generativeai as genai
from datetime import datetime
from duckduckgo_search import DDGS

class SecurityAgent:
    """Specialized ADK Agent for the Cybersecurity Industry."""
    
    def __init__(self, api_key, model_id="gemini-2.0-pro-exp-02-05"):
        genai.configure(api_key=api_key)
        self.model_id = model_id
        
        self.system_instruction = """
        You are the 'Security-ADK' SOC Analyst.
        Focus: Threat hunting, vulnerability analysis, and incident response planning.
        
        PROTOCOLS:
        1. Zero Trust: Assume a stance of default-deny and verify every signal.
        2. Technical Depth: Use CVE IDs, MITRE ATT&CK framework terms, and specific containment strategies.
        3. Compliance: Align recommendations with SOC2, GDPR, and NIST standards.
        
        Current Time: {now}
        """.format(now=datetime.now())
        
        self.model = genai.GenerativeModel(
            model_name=self.model_id,
            tools=[self.search_threat_intel],
            system_instruction=self.system_instruction
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def search_threat_intel(self, query: str):
        """Web search for latest CVEs, threat actor patterns, and security advisories."""
        with DDGS() as ddgs:
            return [r for r in ddgs.text(f"cybersecurity threat intelligence {query}", max_results=5)]

    def run(self, prompt):
        response = self.chat.send_message(prompt)
        return response.text

if __name__ == "__main__":
    key = os.getenv("GEMINI_API_KEY")
    if key:
        agent = SecurityAgent(key)
        print(agent.run("What are the latest zero-day vulnerabilities affecting Linux servers?"))
