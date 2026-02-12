import streamlit as st
from groq import Groq

# Page Setup
st.set_page_config(page_title="Nyaya-AI: Indian Law Assistant", page_icon="⚖️")
st.title("⚖️ Nyaya-AI: Indian Law & Petition Drafter")

# Sidebar for API Key
api_key = st.sidebar.text_input("Apni Groq API Key yahan dalein:", type="password")

if api_key:
    client = Groq(api_key=api_key)

    # Sidebar Options
    mode = st.sidebar.selectbox("Kya karna chahte hain?", ["Legal Advice", "Petition Drafting"])

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat History display
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("Apna sawal likhein ya petition ki details dein..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Logic
        with st.chat_message("assistant"):
            # System Prompt for Legal Context
            system_prompt = "You are an expert Indian Legal Assistant. Knowledgeable in BNS, IPC, and Constitution of India. Provide advice with a disclaimer that you are an AI, not a lawyer. If drafting, use professional legal format."
            
            full_prompt = f"{system_prompt}\nUser Request: {prompt}"
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile", # Super fast and powerful
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.7,
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.warning("Please enter your Groq API Key in the sidebar to start.")
  
