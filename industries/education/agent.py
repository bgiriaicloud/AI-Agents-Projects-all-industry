import os
import google.generativeai as genai
from datetime import datetime
from duckduckgo_search import DDGS

class EducationAgent:
    """Specialized ADK Agent for the Education Industry."""
    
    def __init__(self, api_key, model_id="gemini-2.0-pro-exp-02-05"):
        genai.configure(api_key=api_key)
        self.model_id = model_id
        
        self.system_instruction = """
        You are the 'Education-ADK' Pedagogical Expert.
        Focus: Personalized learning, curriculum design, and automated grading assistance.
        
        PROTOCOLS:
        1. Socratic Method: Encourage students to think for themselves by asking guided questions.
        2. Inclusivity: Design curricula that cater to various learning styles and accessibility needs.
        3. Factual Accuracy: Use tools to verify academic information before providing lesson plans.
        
        Current Time: {now}
        """.format(now=datetime.now())
        
        self.model = genai.GenerativeModel(
            model_name=self.model_id,
            tools=[self.search_academic_resources],
            system_instruction=self.system_instruction
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def search_academic_resources(self, topic: str):
        """Web search for high-quality academic papers, course materials, and factual datasets."""
        with DDGS() as ddgs:
            return [r for r in ddgs.text(f"academic resource and lesson plan {topic}", max_results=5)]

    def run(self, prompt):
        response = self.chat.send_message(prompt)
        return response.text

if __name__ == "__main__":
    key = os.getenv("GEMINI_API_KEY")
    if key:
        agent = EducationAgent(key)
        print(agent.run("Design a 3-week course outline for 10th-grade students on Quantum Physics basics."))
