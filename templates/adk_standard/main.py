import os
import streamlit as st
from agent_factory import ADKAgent
from toolbox import GLOBAL_TOOLBOX

st.set_page_config(page_title="ADK Template Console", layout="wide")

st.title("🛡️ ADK Standard Template v1.1")

# API Configuration
with st.sidebar:
    st.header("ADK Config")
    api_key = st.text_input("Gemini API Key", type="password")
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    
    industry = st.selectbox("Assign Node Type", list(GLOBAL_TOOLBOX.keys()))
    st.info(f"Node active: {industry}")

# Initialization
if "agent" not in st.session_state or st.sidebar.button("Reset Agent"):
    if api_key:
        st.session_state.agent = ADKAgent(
            name=f"{industry.capitalize()}Manager",
            role=f"Expert {industry} Intelligence Node",
            tools=GLOBAL_TOOLBOX[industry]
        )

# UI
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Enter command..."):
    if not api_key:
        st.error("Missing API Key")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("ADK Node processing..."):
                response = st.session_state.agent.process(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
