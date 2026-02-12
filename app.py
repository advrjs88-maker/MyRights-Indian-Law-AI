import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing dependency: Please install 'groq' using 'pip install groq'")
import os

# Page Configuration
st.set_page_config(page_title="MyRights AI", page_icon="⚖️", layout="centered")

# Custom CSS for Professional Legal Look
st.markdown("""
    <style>
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
        padding: 50px;
        border-radius: 2px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 1px solid #cfd8dc;
        margin-top: 20px;
        min-height: 600px;
    }
    .legal-document strong {
        font-weight: bold;
        color: #000;
    }
    .stTextArea textarea {
        border: 2px solid #1e3a8a !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- API KEY HANDLING (Baar baar dalne se bachne ke liye) ---
# Streamlit Secrets (share.streamlit.io settings mein set karein)
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
    st.sidebar.warning("Tip: Settings -> Secrets mein 'GROQ_API_KEY' set karein.")
else:
    st.sidebar.success("API Key loaded from Secrets ✅")

# Branding Header
st.markdown("<h1 style='text-align: center; margin-bottom: 0; color: #1e3a8a;'>MyRights AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #4b5563; margin-top: 0;'>Legal drafting & research system</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 11px; font-weight: bold; color: #6b7280; letter-spacing: 0.2em; text-transform: uppercase;'>Created by R.J. Sharma, Advocate</p>", unsafe_allow_html=True)
st.divider()

# Input UI
user_query = st.text_area("Type your request (e.g., 'Draft a divorce petition', 'Section 498A IPC', 'Maintenance judgments')", 
                         placeholder="Example: Draft a notice for recovery of money...",
                         height=150)

model_choice = st.sidebar.selectbox("Select Intelligence Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])

generate_btn = st.button("EXECUTE COMMAND", use_container_width=True)

# Main Processing Logic
if generate_btn:
    if not api_key:
        st.error("Please provide an API Key in the sidebar or Secrets.")
    elif not user_query:
        st.warning("Search box cannot be empty.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            system_instr = """
            Tum 'MyRights AI' ho, ek professional legal drafting aur research system.
            
            USER INTENT RULES:
            1. AGAR 'PETITION' ya 'DRAFT' ho (STRICT COURT FORMAT): 
               - Court Name (IN THE COURT OF...)
               - Case No. ___ of 202_ (Next line)
               - Petitioner vs Respondent details (Next line)
               - TITLE LINE: "Petition for [Subject] under Section [No] of [Act]"
               - Detailed Numbered paragraphs for facts.
               - PRAYER Clause.
               - VERIFICATION Clause (Next line after prayer).
               - Date: _________ (Next line)
               - Place: _________ (Next line)

            2. AGAR 'SECTION' ya 'ACT' ya 'SEARCH' ho:
               - BARE ACT Book Format: Section Number, Full Text, Sub-sections, Provisos exactly as per law books.
               - CLASSIFICATION TABLE: Cognizable/Non-Cognizable, Bailable/Non-Bailable, Compoundable/Non-Compoundable, Punishment details.
               - Legal Commentary/Explanation and latest Case Laws related to that specific section.

            3. AGAR 'JUDGMENT' ya 'CITATION' ho:
               - Point-wise latest Landmark Judgments with bold Citations.

            FORMATTING MANDATE:
            - Content MUST be JUSTIFIED.
            - ALL LANDMARK JUDGMENTS and CITATIONS (AIR, SCC, etc.) MUST be BOLD (<strong>).
            - Professional Legalese language only.
            """

            with st.spinner("Analyzing legal provisions and drafting..."):
                completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_instr},
                        {"role": "user", "content": user_query}
                    ],
                    model=model_choice,
                )
                
                output_text = completion.choices[0].message.content
                
                # Conversion to HTML for justification and bolding
                parts = output_text.split("**")
                html_formatted = ""
                for i, part in enumerate(parts):
                    if i % 2 == 1:
                        html_formatted += f"<strong>{part}</strong>"
                    else:
                        html_formatted += part
                
                final_html = html_formatted.replace("\n", "<br>")
                
                # Render Document
                st.markdown(f'<div class="legal-document">{final_html}</div>', unsafe_allow_html=True)
                
                # Action Buttons
                st.download_button("Download Document (.txt)", output_text, file_name="MyRights_AI_Output.txt")

        except Exception as e:
            st.error(f"System Error: {str(e)}")

st.divider()
st.caption("Legal Disclaimer: Research generated by AI should be verified by a legal professional before filing.")
