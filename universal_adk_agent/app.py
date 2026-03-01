import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime
import yfinance as yf
from duckduckgo_search import DDGS

# --- ADK CORE COMPONENTS ---

class ADKToolbox:
    @staticmethod
    def get_market_data(ticker: str):
        """Fetches real-time stock data and analyst info."""
        data = yf.Ticker(ticker).info
        return {
            "price": data.get("regularMarketPrice"),
            "recommendation": data.get("recommendationKey"),
            "summary": data.get("longBusinessSummary")[:500] if data.get("longBusinessSummary") else "N/A"
        }

    @staticmethod
    def search_web(query: str):
        """Performs a web search for the latest industry news."""
        with DDGS() as ddgs:
            return [r for r in ddgs.text(query, max_results=3)]

class UniversalADKAgent:
    def __init__(self, api_key, industry, temperature=0.7):
        genai.configure(api_key=api_key)
        self.industry = industry
        self.tools = self._get_tools_for_industry()
        
        system_instruction = f"""
        You are the 'Universal ADK Agent' operating in {self.industry} mode.
        Instructions:
        1. Use available tools for real-time verification.
        2. Adopt the specific persona of a {self.industry} expert.
        3. For Finance: Focus on quantitative accuracy.
        4. For Healthcare: Prioritize safety guidelines.
        5. For Legal: Maintain high-precision document logic.
        Current Time: {datetime.now()}
        """
        
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-pro-exp-02-05", # Top-tier reasoning
            tools=self.tools,
            system_instruction=system_instruction,
            generation_config={"temperature": temperature}
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def _get_tools_for_industry(self):
        if self.industry == "Financial Analyst":
            return [ADKToolbox.get_market_data, ADKToolbox.search_web]
        return [ADKToolbox.search_web]

    def ask(self, prompt):
        response = self.chat.send_message(prompt)
        return response.text

# --- STREAMLIT UI ---

st.set_page_config(page_title="Universal ADK Hub", page_icon="🌐", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: white; }
    .header { background: linear-gradient(90deg, #1e40af, #3b82f6); padding: 2rem; border-radius: 15px; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"><h1>ADK Universal Intelligence Hub</h1><p>Integrated Node for All Industries</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.title("🛡️ ADK Configuration")
    api_key = st.text_input("Gemini API Key", type="password")
    industry = st.selectbox("Assign Industry Node", ["General Research", "Financial Analyst", "Healthcare Expert", "Legal Counsel", "Security Specialist"])
    temp = st.slider("Reasoning Depth", 0.0, 1.0, 0.7)

# Session State
if "adk_chat" not in st.session_state:
    st.session_state.adk_chat = []

if "agent" not in st.session_state or st.sidebar.button("Re-init Agent"):
    if api_key:
        st.session_state.agent = UniversalADKAgent(api_key, industry, temp)

# Chat Loop
for msg in st.session_state.adk_chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Dispatch command..."):
    if not api_key:
        st.error("Missing API Key")
    else:
        st.session_state.adk_chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(f"ADK {industry} Node Processing..."):
                try:
                    response = st.session_state.agent.ask(prompt)
                    st.markdown(response)
                    st.session_state.adk_chat.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"ADK Node Error: {e}")
