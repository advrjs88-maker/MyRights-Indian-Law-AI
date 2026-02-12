import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="MyRights Legal AI Assistance", page_icon="⚖️", layout="wide")

# App Name
st.title("⚖️ MyRights Legal AI Assistance")
st.caption("Professional Indian Legal Drafting & Research Portal")

# Sidebar for API Key
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

if api_key:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Search Bar
    if prompt := st.chat_input("Search Section, Draft Petition, or Legal Notice..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # STRICT LEGAL INSTRUCTIONS - NO HINDI, NO CONVERSATION
            instructions = """
            You are 'MyRights Legal AI Assistance', a Senior Indian Legal Expert. 
            Strictly follow these response protocols:
            1. LANGUAGE: Use ONLY professional English. Do not use Hindi or any other language.
            2. PETITIONS: Start directly with 'IN THE COURT OF...'. Use standard court formatting with [Bracketed Placeholders] for facts.
            3. LEGAL NOTICE: Provide a formal notice from an Advocate's perspective. Include 'Under instructions from my client...'
            4. BARE ACT/SECTIONS: Provide the exact legal provision, details of the latest 2023-24 amendments (BNS/BNSS/BSA), and cite at least 2 landmark Supreme Court/High Court judgments.
            5. DEEDS/AGREEMENTS: Provide a complete, ready-to-use legal draft.
            6. NO PROAMBLE: Do not say 'Sure', 'I can help', 'Here is your draft', or 'Disclaimer'. Start directly with the legal text.
            7. NO CONVERSATION: Do not engage in small talk. Focus only on the legal output requested.
            """
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1, # Lowest temperature for maximum accuracy and zero creativity
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("👈 Please enter your Groq API Key in the sidebar to activate MyRights Legal AI.")
    
