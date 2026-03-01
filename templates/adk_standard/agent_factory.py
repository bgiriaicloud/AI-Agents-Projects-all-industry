import google.generativeai as genai
from datetime import datetime

class ADKAgent:
    def __init__(self, name, role, tools=None, model_id="gemini-2.0-pro-exp-02-05"):
        self.name = name
        self.role = role
        self.tools = tools or []
        self.model_id = model_id
        self.system_instruction = self._build_system_instruction()
        
        self.model = genai.GenerativeModel(
            model_name=self.model_id,
            tools=self.tools,
            system_instruction=self.system_instruction
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def _build_system_instruction(self):
        return f"""
        Name: {self.name}
        Role: {self.role}
        Standard: ADK/2026.03
        
        You are a highly specialized AI Agent. 
        Always provide technical, precise, and verified information.
        If tools are available, use them to provide real-time data.
        Current Time: {datetime.now()}
        """

    def process(self, prompt):
        response = self.chat.send_message(prompt)
        return response.text
