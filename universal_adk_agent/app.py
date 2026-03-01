import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime

# --- SETTINGS ---
# Using the latest available powerful model (Gemini 2.0 Pro)
# Note: Gemini 2.4 is a futuristic placeholder, using current top-tier 2.0 Pro Experimental.
MODEL_NAME = "gemini-2.0-pro-exp-02-05" 

st.set_page_config(page_title="Universal ADK Agent", page_icon="🌐", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .main { background-color: #0b0e14; }
    .stTextInput>div>div>input { background-color: #1c2128; color: white; border: 1px solid #30363d; }
    .stSelectbox>div>div>div { background-color: #1c2128; color: white; }
    .agent-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        text-align: center;
    }
    .industry-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        background-color: #238636;
        color: white;
        font-size: 0.8em;
        margin-right: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: AUTH & CONTEXT ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg", width=150)
    st.title("ADK Hub Control")
    api_key = st.text_input("Gemini API Key", type="password", key="adk_api_key")
    
    st.divider()
    st.markdown("### 🎯 Industry Persona")
    active_industry = st.selectbox(
        "Current Active Node",
        ["Universal Architect", "Healthcare Expert", "Financial Analyst", "Security Analyst", "Retail Strategist", "Logistics Optimizer", "Legal Counsel"]
    )
    
    st.markdown("### 🚀 Model Configuration")
    st.info(f"Model: {MODEL_NAME}")
    temperature = st.slider("Creativity (Temperature)",0.0, 1.0, 0.7)

# --- AGENT LOGIC (ADK STYLE) ---
class UniversalADKAgent:
    def __init__(self, api_key, industry_context, temperature):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config={"temperature": temperature}
        )
        self.industry = industry_context
        
    def generate_system_instruction(self):
        base = """You are the 'Universal ADK Agent', a master-class AI capable of cross-industry intelligence. 
        Current Timestamp: {now}
        
        Your architecture:
        - Brain: Gemini 2.0 Pro
        - Mode: {mode}
        
        Guidelines:
        1. Access the 'Global Industry Blueprint' knowledge base.
        2. If in a specific industry mode, prioritize that sector's terminology and constraints.
        3. Use a structured, professional tone.
        4. For Healthcare: Prioritize HIPAA-compliant logic and safety.
        5. For Finance: Prioritize real-time market awareness and risk analysis.
        6. For Security: Focus on Zero-Trust protocols and threat mitigation.
        """.format(now=datetime.now(), mode=self.industry)
        return base

    def run(self, prompt, history):
        chat = self.model.start_chat(history=history)
        full_prompt = f"{self.generate_system_instruction()}\n\nUser Question: {prompt}"
        response = chat.send_message(full_prompt)
        return response.text

# --- APP UI ---
st.markdown('<div class="agent-header"><h1>One-Agent-For-All (Universal ADK)</h1><p>The Modular Hub for Modern Industry Solutions</p></div>', unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display welcome message based on industry
if not st.session_state.chat_history:
    with st.chat_message("assistant"):
        st.markdown(f"Greetings. I am your **Universal ADK Agent** currently operating in **{active_industry}** mode. How can I assist you in your mission today?")

# Render Chat
for message in st.session_state.chat_history:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Dispatch command to Universal Agent..."):
    if not api_key:
        st.warning("Please provide a valid Gemini API Key in the sidebar.")
    else:
        # Add to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Agent Response
        with st.chat_message("assistant"):
            agent = UniversalADKAgent(api_key, active_industry, temperature)
            # Convert session state history to genai format
            formatted_history = []
            for msg in st.session_state.chat_history[:-1]:
                formatted_history.append({"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]})
            
            with st.spinner(f"ADK Hub: Processing request via {active_industry} Node..."):
                try:
                    res_text = agent.run(prompt, formatted_history)
                    st.markdown(res_text)
                    st.session_state.chat_history.append({"role": "assistant", "content": res_text})
                except Exception as e:
                    st.error(f"ADK Protocol Error: {str(e)}")

# --- FOOTER ---
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("Architecture: Multi-Node ADK")
with col2:
    st.caption(f"Engine: {MODEL_NAME}")
with col3:
    st.caption("Status: Optimal")
