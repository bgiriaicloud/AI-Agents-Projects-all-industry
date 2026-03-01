import os
import google.generativeai as genai
from datetime import datetime
from .tools import FULL_CAPABILITIES

class OmniAgent:
    """The 'One' Agent for all industries built on ADK principles."""
    
    def __init__(self, api_key, model_id="gemini-2.0-pro-exp-02-05"):
        genai.configure(api_key=api_key)
        self.model_id = model_id
        
        # Comprehensive System Instruction for Universal Intelligence
        self.system_instruction = """
        You are the 'OmniAgent-ADK', the definitive AI Agent for all global industries.
        Your architectural design is 'One-for-All', meaning you dynamically adjust your reasoning based on the industry mentioned in the user's prompt.
        
        CROSS-INDUSTRY PROTOCOLS:
        1. FINANCE: Prioritize quantitative data and risk assessment. Use the finance_tool.
        2. HEALTHCARE: Provide research-backed insights. Use healthcare_tool. REMINDER: You are an AI, not a doctor.
        3. MANUFACTURING: Monitor IoT signals and predict downtime. Use manufacturing_tool.
        4. GENERAL RESEARCH: Use research_tool for real-time web verification.
        
        STANDARD OPERATING PROCEDURE:
        - Always use a tool if the user asks for real-time data.
        - provide structured, professional, and cited responses.
        - Maintain a persona of a 'Principal Consultant' in the relevant industry.
        
        Current System Time: {now}
        """.format(now=datetime.now())
        
        self.model = genai.GenerativeModel(
            model_name=self.model_id,
            tools=FULL_CAPABILITIES,
            system_instruction=self.system_instruction
        )
        # Start a stateful chat session with automatic tool calling enabled
        self.chat_session = self.model.start_chat(enable_automatic_function_calling=True)

    def dispatch(self, user_prompt):
        """Sends a message to the OmniAgent and returns the response."""
        response = self.chat_session.send_message(user_prompt)
        return response.text
