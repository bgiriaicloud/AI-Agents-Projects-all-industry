import os
import google.generativeai as genai
from datetime import datetime
import random

class ManufacturingAgent:
    """Specialized ADK Agent for Manufacturing & Industrial IoT."""
    
    def __init__(self, api_key, model_id="gemini-2.0-pro-exp-02-05"):
        genai.configure(api_key=api_key)
        self.model_id = model_id
        
        self.system_instruction = """
        You are the 'Manufacturing-ADK' Operations Manager.
        Focus: Predictive maintenance, factory floor safety, and supply chain synchronization.
        
        PROTOCOLS:
        1. Operational Reliability: Focus on OEE (Overall Equipment Effectiveness) and downtime reduction.
        2. Maintenance: Prioritize preventive and predictive strategies over reactive ones.
        3. Safety First: Any anomaly in worker safety or machine temp should be flagged as critical.
        
        Current Time: {now}
        """.format(now=datetime.now())
        
        self.model = genai.GenerativeModel(
            model_name=self.model_id,
            tools=[self.simulate_iot_sensors],
            system_instruction=self.system_instruction
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def simulate_iot_sensors(self, machine_id: str):
        """Simulates real-time IoT sensor data (temp, vibration, pressure) for factory equipment."""
        return {
            "machine_id": machine_id,
            "core_temp_c": f"{random.randint(65, 110)}",
            "vibration_rms": f"{round(random.uniform(0.1, 5.0), 2)} mm/s",
            "pressure": f"{random.randint(2000, 5000)} kPa",
            "status": "Warning" if random.random() > 0.8 else "Healthy"
        }

    def run(self, prompt):
        response = self.chat.send_message(prompt)
        return response.text

if __name__ == "__main__":
    key = os.getenv("GEMINI_API_KEY")
    if key:
        agent = ManufacturingAgent(key)
        print(agent.run("Analyze the health status of Machine-Line-A3."))
