import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing dependency: Please install 'groq' using 'pip install groq'")
import os

# Page Configuration
st.set_page_config(page_title="MyRights AI", page_icon="⚖️", layout="centered")

# Custom CSS for Legal Formatting
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');
    
    .main {
        background-color: #f8fafc;
    }
    .legal-document {
        font-family: 'Times New Roman', Times, serif;
        text-align: justify;
        line-height: 1.6;
        color: #1a1a1a;
        background-color: white;
        padding: 45px;
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 1px solid #d1d5db;
        margin-top: 20px;
    }
    .legal-document strong {
        font-weight: bold;
        color: #000;
    }
    .search-box {
        border: 2px solid #1e3a8a !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Branding Header
st.markdown("<h1 style='text-align: center; margin-bottom: 0; color: #1e3a8a;'>MyRights AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #4b5563; margin-top: 0;'>Legal drafting & research system</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 11px; font-weight: bold; color: #6b7280; letter-spacing: 0.2em; text-transform: uppercase;'>Created by R.J. Sharma, Advocate</p>", unsafe_allow_html=True)
st.divider()

# Groq API Configuration in Sidebar
api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
model_choice = st.sidebar.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])

# Unified Smart Input Box
user_query = st.text_area("Search or Type your Drafting Command", 
                         placeholder="e.g., 'Draft a petition for divorce' OR 'Draft a notice for recovery' OR 'Section 138 NI Act details' OR 'Landmark judgments on maintenance'",
                         height=120)

generate_btn = st.button("SEARCH / GENERATE", use_container_width=True)

# Logic Section
if generate_btn:
    if not api_key:
        st.error("Kripya Groq API Key sidebar mein enter karein.")
    elif not user_query:
        st.warning("Kripya search box mein kuch likhein.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            # Smart System Prompt based on input detection
            system_instr = """
            Tum ek expert legal system 'MyRights AI' ho. User ke query ke hisaab se behave karo:
            
            1. Agar 'Draft a Petition/Draft' keyword ho: Toh Standard Judicial/Court Format mein draft banao (Jurisdiction, Parties, Numbered Paras, Prayer).
            2. Agar 'Notice' keyword ho: Toh Formal Legal Notice (Advocate style) banao (Under instructions, 15/30 days demand).
            3. Agar 'Deed/Agreement' keyword ho: Toh professional Agreement format banao (Recitals, Clauses, Termination).
            4. Agar 'Section', 'Act', ya Law related query ho: Toh 'Bare Act & Research' style mein point-wise explanation do.
            5. MANDATORY: Har draft ya research ke niche 'LANDMARK JUDGMENTS & CITATIONS' ki heading dalo aur kam se kam 3 latest/important judgments likho.
            
            STRICT FORMATTING RULES:
            - Content hamesha JUSTIFY alignment mein hona chahiye.
            - Sare LANDMARK JUDGMENTS aur CITATIONS (e.g., AIR, SCC) ko BOLD karo.
            - Poora text Point-wise aur Number-wise hona chahiye.
            - Har point ek naye line se shuru hoga.
            - Professional Legal language use karo.
            """

            with st.spinner("AI Legal Research and Drafting in progress..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_instr},
                        {"role": "user", "content": user_query}
                    ],
                    model=model_choice,
                )
                
                legal_text = chat_completion.choices[0].message.content
                
                # Robust Markdown to HTML conversion for bold and justification
                parts = legal_text.split("**")
                html_parts = []
                for i, part in enumerate(parts):
                    if i % 2 == 1:
                        html_parts.append(f"<strong>{part}</strong>")
                    else:
                        html_parts.append(part)
                
                final_html = "".join(html_parts).replace("\n", "<br>")
                
                # Output Section
                st.markdown(f"""
                    <div class="legal-document">
                        {final_html}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Download
                st.download_button(
                    label="Download Document",
                    data=legal_text,
                    file_name="MyRights_AI_Draft.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"Error: {str(e)}")

st.divider()
st.caption("Legal Disclaimer: Yeh system research purposes ke liye hai. Professional use se pehle Advocate se salaah zaroori hai.")
