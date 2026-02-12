import streamlit as st
from groq import Groq

# Page Setup
st.set_page_config(page_title="MyRights Legal AI Assistance", layout="wide")

# Custom CSS for Professional Formatting
st.markdown("""
    <style>
    .reportview-container .main .block-container { padding-top: 1rem; }
    .legal-body { text-align: justify; line-height: 1.6; font-family: 'Times New Roman', Times, serif; }
    .center-text { text-align: center; font-weight: bold; text-transform: uppercase; }
    .bold-cite { font-weight: bold; color: #1a1a1a; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ MyRights Legal AI Assistance")

# --- INPUT SECTION AT TOP ---
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

if api_key:
    client = Groq(api_key=api_key)
    
    # Search Bar at Top
    prompt = st.chat_input("Search Section, Draft Petition, or Legal Notice...")

    if prompt:
        with st.spinner("Processing Legal Draft..."):
            # SYSTEM INSTRUCTIONS
            instructions = """
            You are 'MyRights Legal AI Assistance'. Strictly follow these formatting rules:
            1. LANGUAGE: English only.
            2. IF PETITION: Use this EXACT header:
               [CENTER] IN THE COURT OF [COURT NAME], [CITY]
               [CENTER] Case No. __________ of [YEAR]
               
               [Petitioner Name/Address] ... Petitioner
               [CENTER] VERSUS
               [Respondent Name/Address] ... Respondent
               
               [CENTER] [TITLE OF PETITION IN CAPITAL]
               
               Respected Sir,
               Most Respectfully showeth-
            3. NUMBERING: Start every new point/paragraph from a NEW LINE.
            4. CITATIONS: Landmark judgments must be **BOLD**. Example: **Kesavananda Bharati v. State of Kerala (1973)**.
            5. AMENDMENTS: Mention 2023-24 changes (BNS/BNSS) only if confirmed. No hallucinations.
            6. ALIGNMENT: The output for body text must be structured for JUSTIFIED alignment.
            7. NO HEADER FOR SECTIONS: If user asks for a Section/Act, do NOT use 'In the Court of'. Start directly with the Provision.
            """

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
            )
            
            response = completion.choices[0].message.content
            
            # --- OUTPUT SECTION BELOW ---
            st.markdown("---")
            # Using a container for Justified alignment
            st.markdown(f'<div class="legal-body">{response.replace("\n", "<br>")}</div>', unsafe_allow_html=True)

else:
    st.info("👈 Please enter your Groq API Key in the sidebar to start.")
    
