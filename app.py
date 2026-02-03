import streamlit as st
import os
from openai import OpenAI

# --- CONFIGURATION ---
# Get API key from Streamlit secrets or environment variable
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))

# --- PAGE SETUP ---    
st.set_page_config(page_title="Legal Mind AI", page_icon="⚖️")

st.title("⚖️ AI Legal Consultant")
st.markdown("Ask questions about Supreme Court judgments (Workstream 2 Pilot).")

# --- CONSULTANT BOT LOGIC ---
def consultant_bot(user_query):
    """
    Process legal consultation queries using OpenAI.
    This replaces the n8n webhook with direct AI integration.
    """
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # System prompt for legal consultation
        system_prompt = """You are an expert legal AI consultant specializing in Supreme Court judgments and Indian law.
        
Your role is to:
- Analyze legal questions with precision and clarity
- Reference relevant Supreme Court judgments when applicable
- Provide well-structured, professional legal insights
- Cite case law and legal principles accurately
- Explain complex legal concepts in accessible language

Always maintain a professional tone and acknowledge when a question requires consultation with a licensed attorney."""

        # Create chat completion
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using cost-effective model, can upgrade to gpt-4 if needed
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract the AI response
        ai_answer = response.choices[0].message.content
        return ai_answer
        
    except Exception as e:
        return f"Error processing your query: {str(e)}\n\nPlease ensure your OpenAI API key is configured in Streamlit secrets."

# --- CHAT INTERFACE ---
# Check if API key is configured
if not OPENAI_API_KEY:
    st.warning("⚠️ OpenAI API key not configured. Please add it to Streamlit secrets or environment variables.")
    st.info("""
    **To configure on Streamlit Cloud:**
    1. Go to your app settings
    2. Click on 'Secrets'
    3. Add: `OPENAI_API_KEY = "your-api-key-here"`
    """)

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

    # Call Consultant Bot
    with st.chat_message("assistant"):
        with st.spinner("Analyzing case files..."):
            # Get AI response using the consultant_bot function
            ai_answer = consultant_bot(prompt)
            st.markdown(ai_answer)
            # Save to history
            st.session_state.messages.append({"role": "assistant", "content": ai_answer})
