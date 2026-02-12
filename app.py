import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing dependency: Please install 'groq' using 'pip install groq'")
import os
import re

# Page Configuration
st.set_page_config(page_title="MyRights AI", page_icon="⚖️", layout="centered")

# --- ADVANCED CSS TO REMOVE ALL STREAMLIT BRANDING ---
# Ye code footer, header, menu aur extra padding ko puri tarah khatam kar dega
hide_st_style = """
            <style>
            /* Hide Streamlit components */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            #stDecoration {display:none;}
            [data-testid="stHeader"] {display:none;}
            [data-testid="stFooter"] {display:none;}
            [data-testid="stToolbar"] {display:none;}
            
            /* Remove extra padding from top */
            .st-emotion-cache-18ni73i {padding-top: 0rem;}
            .st-emotion-cache-z5fcl4 {padding-top: 0rem;}
            
            /* Professional Typography */
            @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');
            
            .main {
                background-color: #f1f5f9;
            }
            .legal-document {
                font-family: 'Times New Roman', Times, serif;
                text-align: justify;
                line-height: 1.6;
                color: #1a1a1a;
                background-color: white;
                padding: 40px;
                border-radius: 4px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                border: 1px solid #cfd8dc;
                margin-top: 20px;
                white-space: pre-wrap;
            }
            .legal-document strong {
                font-weight: bold;
                color: #000;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- API KEY HANDLING ---
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
else:
    st.sidebar.success("System Ready ✅")

# Branding Header
st.markdown("<h1 style='text-align: center; margin-bottom: 0; color: #1e3a8a; padding-top: 0;'>MyRights AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #4b5563; margin-top: 0;'>Legal drafting & research system</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 11px; font-weight: bold; color: #6b7280; letter-spacing: 0.2em; text-transform: uppercase;'>Created by R.J. Sharma, Advocate</p>", unsafe_allow_html=True)
st.divider()

# Input UI
user_query = st.text_area("Search / Draft Command", 
                         placeholder="Example: Draft a notice for recovery of money or search Section 302 IPC...",
                         height=150)

model_choice = st.sidebar.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])

generate_btn = st.button("EXECUTE COMMAND", use_container_width=True)

# Main Processing Logic
if generate_btn:
    if not api_key:
        st.error("Please provide an API Key.")
    elif not user_query:
        st.warning("Search box cannot be empty.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            # Formatting instructions based on legal standards
            system_instr = """
            Tum 'MyRights AI' ho.
            
            1. LEGAL NOTICE: Heading bold/center. Ref No, Date, Subject (Bold/Underlined). Opening clause mandatory. Numbered Paras. Demand Clause with deadline. Sign-off with 'WITHOUT PREJUDICE'.
            2. PETITION: Court Name -> Case No -> Parties -> Title -> Facts (Numbered) -> Prayer -> Verification -> Date -> Place.
            3. BARE ACT: Section text, Provisos, Classification Table (Bailable, Cognizable etc.), Commentary, and Landmark Judgments.

            STRICT: Text JUSTIFIED, Citations BOLD.
            """

            with st.spinner("Processing..."):
                completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_instr},
                        {"role": "user", "content": user_query}
                    ],
                    model=model_choice,
                )
                
                output_text = completion.choices[0].message.content
                # Safer HTML parsing
                safe_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', output_text)
                safe_html = safe_html.replace("\n", "<br>")
                
                st.markdown(f'<div class="legal-document">{safe_html}</div>', unsafe_allow_html=True)
                st.download_button("Download Document", output_text, file_name="MyRights_Output.txt")

        except Exception as e:
            st.error(f"Error: {str(e)}")

st.divider()
st.caption("Legal Disclaimer: Verified research system for advocates.")
