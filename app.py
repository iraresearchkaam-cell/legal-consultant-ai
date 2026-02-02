import streamlit as st
import requests

# --- CONFIGURATION ---
# Paste your N8N Production Webhook URL here
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/consultant-bot"

# --- PAGE SETUP ---
st.set_page_config(page_title="Legal Mind AI", page_icon="⚖️")

st.title("⚖️ AI Legal Consultant")
st.markdown("Ask questions about Supreme Court judgments (Workstream 2 Pilot).")

# --- CHAT INTERFACE ---
# 1. Initialize chat history if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Handle new user input
if prompt := st.chat_input("Ex: Can a railway penalty be imposed after delivery?"):
    # Display user message immediately
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call N8N Backend
    with st.chat_message("assistant"):
        with st.spinner("Analyzing case files..."):
            try:
                # Send POST request to n8n
                response = requests.post(
                    N8N_WEBHOOK_URL, 
                    json={"chatInput": prompt}  # This matches the variable name expected by n8n
                )
                
                if response.status_code == 200:
                    # Extract answer from JSON
                    ai_answer = response.json().get("answer", "Error: No answer field found.")
                    st.markdown(ai_answer)
                    # Save to history
                    st.session_state.messages.append({"role": "assistant", "content": ai_answer})
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
                    
            except Exception as e:
                st.error(f"Connection Error: {e}")
