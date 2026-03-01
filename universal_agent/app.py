import streamlit as st
import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGo
from agno.tools.googlesearch import GoogleSearch
from agno.tools.file import FileTools

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Universal Industry AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- STYLING ---
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .industry-card {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #1e293b;
        background-color: #161b22;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #2563eb;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR & SETUP ---
with st.sidebar:
    st.title("⚙️ Universal Configuration")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
    
    st.divider()
    st.markdown("### 🏭 Select Industry Context")
    industry = st.selectbox(
        "Choose Vertical",
        ["General", "Finance", "Healthcare", "Legal", "Cybersecurity", "Retail", "Manufacturing"]
    )
    
    st.divider()
    st.markdown("### 🛠️ Active Tools")
    st.checkbox("Web Search (DuckDuckGo)", value=True)
    st.checkbox("Financial Data (yFinance)", value=(industry == "Finance"))
    st.checkbox("File System Access", value=True)

# --- MAIN INTERFACE ---
st.title("🤖 One-for-All: Universal Industry Agent")
st.markdown(f"**Current Mode:** `{industry} specialist` | Powered by Gemini 2.0 Pro")

# Define Agent Logic based on Industry
def get_agent(industry_type):
    tools = [DuckDuckGo(), FileTools()]
    
    if industry_type == "Finance":
        tools.append(YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True))
    
    instructions = [
        f"You are a world-class expert in {industry_type}.",
        "Provide professional, data-backed insights.",
        "Use your tools whenever you need real-time data or file operations.",
        "Always cite your sources.",
    ]
    
    if industry_type == "Healthcare":
        instructions.append("Focus on medical accuracy and mention that you are an AI, not a doctor.")
    elif industry_type == "Legal":
        instructions.append("Analyze documents with high precision and focus on risk mitigation.")
    elif industry_type == "Cybersecurity":
        instructions.append("Analyze threats technically and provide containment strategies.")

    return Agent(
        name=f"Universal {industry_type} Agent",
        model=Gemini(id="gemini-2.0-flash-exp"), # Fast and capable
        tools=tools,
        instructions=instructions,
        show_tool_calls=True,
        markdown=True,
    )

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask anything..."):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            agent = get_agent(industry)
            with st.spinner(f"Agent thinking in {industry} mode..."):
                response = agent.run(prompt)
                st.markdown(response.content)
                st.session_state.messages.append({"role": "assistant", "content": response.content})

# --- FOOTER ---
st.divider()
st.caption("Universal Agent Framework v1.0 | Ready for Deployment")
