import streamlit as st
try:
    from groq import Groq
except ImportError:
    st.error("Missing dependency: Please install 'groq' using 'pip install groq'")
import os

# Page Configuration
st.set_page_config(page_title="MyRights AI", page_icon="⚖️", layout="centered")

# Custom CSS for Legal Formatting (Justified Text & Times New Roman)
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
        padding: 40px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }
    .legal-document strong {
        font-weight: bold;
        color: #000;
    }
    h1, h2, h3 {
        color: #1e3a8a !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Branding Header
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>MyRights AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #4b5563; margin-top: 0;'>Legal drafting & research system</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 10px; font-weight: bold; color: #6b7280; letter-spacing: 0.2em; text-transform: uppercase;'>Created by R.J. Sharma, Advocate</p>", unsafe_allow_html=True)
st.divider()

# Input Section
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        category = st.selectbox(
            "Select Category",
            [
                "1. Pleading & Petition",
                "2. formal Legal Notice",
                "3. Deed & Agreement",
                "4. Bare Act & Legal Research",
                "5. Landmark Judgement & Citation"
            ]
        )
        
    with col2:
        topic = st.text_input("Subject / Legal Provision", placeholder="e.g. Section 138 NI Act")

    facts = st.text_area("Facts / Points to be Included", height=150, placeholder="Case ke facts aur points yahan likhein...")

    # Groq API Key Configuration
    api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
    model_choice = st.sidebar.selectbox("Choose Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"])
    
    generate_btn = st.button("GENERATE LEGAL TEXT", use_container_width=True)

# Logic Section
if generate_btn:
    if not api_key:
        st.error("Kripya Groq API Key sidebar mein enter karein.")
    elif not topic or not facts:
        st.warning("Kripya Subject aur Facts dono bharein.")
    else:
        try:
            # Initialize Groq client
            client = Groq(api_key=api_key)
            
            # Formatting Instructions
            prompts = {
                "1. Pleading & Petition": "Draft a Pleading & Petition. Use court format: jurisdiction, parties, numbered paragraphs for facts, legal grounds, and prayer clause.",
                "2. formal Legal Notice": "Draft a formal Legal Notice. Include Ref No, Date, Recipient, 'Under Instructions' clause, facts, breach, 15/30 days demand, and legal warning.",
                "3. Deed & Agreement": "Draft a Deed & Agreement. Include Title, Date, Parties, Recitals (Whereas clauses), Terms, Termination, and Jurisdiction.",
                "4. Bare Act & Legal Research": "Provide Bare Act details. Break down sections point-wise like law books. Explain provisions in detail.",
                "5. Landmark Judgement & Citation": "Provide Landmark Judgement & Citation. Summarize ratio decidendi point-wise."
            }

            system_instr = f"{prompts[category]} STRICT RULES: Text must be JUSTIFIED. ALL LANDMARK JUDGEMENTS & CITATIONS MUST BE BOLD. Use point-wise and number-wise structure. Each point starts on a NEW LINE. Use professional legal language."

            with st.spinner("Groq AI drafting process mein hai..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_instr},
                        {"role": "user", "content": f"Subject: {topic}\nFacts: {facts}"}
                    ],
                    model=model_choice,
                )
                
                legal_text = chat_completion.choices[0].message.content
                
                # Output Section
                st.subheader("Generated Legal Draft")
                
                # Formatting Markdown Bold to HTML Strong
                # This ensures the 'BOLD' requirement is rendered correctly in the justified div
                formatted_text = legal_text.replace("**", "<strong>", 1)
                while "**" in formatted_text:
                    if "<strong>" in formatted_text.split("**")[-1]: # check odd/even
                        formatted_text = formatted_text.replace("**", "</strong>", 1)
                    else:
                        formatted_text = formatted_text.replace("**", "<strong>", 1)
                
                # Correcting simple replacement for reliable bolding
                parts = legal_text.split("**")
                html_parts = []
                for i, part in enumerate(parts):
                    if i % 2 == 1:
                        html_parts.append(f"<strong>{part}</strong>")
                    else:
                        html_parts.append(part)
                
                final_html = "".join(html_parts).replace("\n", "<br>")
                
                st.markdown(f"""
                    <div class="legal-document">
                        {final_html}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.download_button(
                    label="Download Draft",
                    data=legal_text,
                    file_name=f"{topic}_legal_draft.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"Groq API Error: {str(e)}")

# Footer
st.divider()
st.caption(f"MyRights AI v2.0 | Powered by Groq | Created by R.J. Sharma, Advocate")
