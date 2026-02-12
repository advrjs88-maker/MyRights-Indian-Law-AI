import streamlit as st
try:
    import openai
except ImportError:
    st.error("Missing dependency: Please install 'openai' using 'pip install openai'")
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

    facts = st.text_area("Facts / Points to be Included", height=150, placeholder="Yahan case ke facts aur points likhein...")

    # API Key Configuration (Streamlit Secrets ya Sidebar)
    api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
    
    generate_btn = st.button("GENERATE LEGAL TEXT", use_container_width=True)

# Logic Section
if generate_btn:
    if not api_key:
        st.error("Kripya OpenAI API Key enter karein.")
    elif not topic or not facts:
        st.warning("Kripya Subject aur Facts dono bharein.")
    else:
        try:
            # Initialize client for OpenAI v1.0.0+
            client = openai.OpenAI(api_key=api_key)
            
            # Formatting Instructions based on Category
            prompts = {
                "1. Pleading & Petition": "Draft a Pleading & Petition. Use court format: jurisdiction, parties, numbered paragraphs for facts, legal grounds, and prayer clause.",
                "2. formal Legal Notice": "Draft a formal Legal Notice. Include Ref No, Date, Recipient, 'Under Instructions' clause, facts, breach, 15/30 days demand, and legal warning.",
                "3. Deed & Agreement": "Draft a Deed & Agreement. Include Title, Date, Parties, Recitals (Whereas clauses), Terms, Termination, and Jurisdiction.",
                "4. Bare Act & Legal Research": "Provide Bare Act details. Break down sections point-wise like law books. Explain provisions in detail.",
                "5. Landmark Judgement & Citation": "Provide Landmark Judgement & Citation. Summarize ratio decidendi point-wise."
            }

            system_instr = f"{prompts[category]} STRICT RULES: Text must be JUSTIFIED. ALL LANDMARK JUDGEMENTS & CITATIONS MUST BE BOLD. Use point-wise and number-wise structure. Each point starts on a NEW LINE. Use professional legal language."

            with st.spinner("AI legal draft taiyar kar raha hai..."):
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_instr},
                        {"role": "user", "content": f"Subject: {topic}\nFacts: {facts}"}
                    ]
                )
                
                legal_text = response.choices[0].message.content
                
                # Output Section
                st.subheader("Generated Legal Draft")
                
                # Formatting Markdown Bold to HTML Strong
                formatted_text = legal_text.replace("**", "<strong>").replace("**", "</strong>")
                formatted_text = formatted_text.replace("\n", "<br>")
                
                st.markdown(f"""
                    <div class="legal-document">
                        {formatted_text}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.download_button(
                    label="Download as Text File",
                    data=legal_text,
                    file_name=f"{topic}_draft.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.caption("Note: Yeh AI-generated draft hai. Kripya use karne se pehle legal review zaroori hai.")
