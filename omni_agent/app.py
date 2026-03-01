import streamlit as st
from agent import OmniAgent

# --- UI CONFIG ---
st.set_page_config(
    page_title="OmniAgent-ADK | One-for-All",
    page_icon="👑",
    layout="wide"
)

# --- MODERN STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; color: white; }
    .omni-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #3b82f6;
        text-align: center;
        margin-bottom: 25px;
    }
    .status-tag {
        color: #10b981;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="omni-box"><h1>👑 OmniAgent - The Universal ADK</h1><p>Single Master Intelligence for All 500+ Industry Use Cases</p><div class="status-tag">● Protocol: ADK/2026.03 Active</div></div>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg", width=100)
    st.title("Hub Controls")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    
    st.divider()
    st.markdown("### 📊 Capabilities")
    st.success("✅ Multi-Industry Tools Active")
    st.success("✅ Auto-Function Calling Enabled")
    st.success("✅ Gemini 2.0 Pro Engine")
    
    if st.button("🔄 Clear System State"):
        st.session_state.messages = []
        if "agent" in st.session_state:
             del st.session_state["agent"]
        st.rerun()

# --- AGENT INITIALIZATION ---
if "agent" not in st.session_state:
    if api_key:
        with st.spinner("Initializing OmniAgent Architecture..."):
            st.session_state.agent = OmniAgent(api_key)

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversion
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Command Input
if prompt := st.chat_input("Dispatch command (e.g., Analyze AAPL stock or research 5G impact on factory floors)"):
    if not api_key:
        st.error("Missing ADK Authentication Key. Please provide your Gemini API Key in the sidebar.")
    else:
        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Assistant response
        with st.chat_message("assistant"):
            with st.spinner("OmniAgent: Reasoning across industrial nodes..."):
                try:
                    response = st.session_state.agent.dispatch(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"OmniAgent Protocol Failure: {e}")

# --- FOOTER ---
st.divider()
st.caption("Developed with ADK (Agentic Development Kit) | Powered by Google Gemini")
