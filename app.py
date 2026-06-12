import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load Environment & Initialize Hugging Face Client via OpenAI SDK
load_dotenv()
hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    st.warning("⚠️ HF_TOKEN not found in .env file. Please enter your Hugging Face token below to run the app:")
    hf_token = st.text_input("Enter Hugging Face API Token (hf_...):", type="password")

# Point the OpenAI client to Hugging Face's serverless router
client = OpenAI(
    base_url="https://router.huggingface.co/v1/",
    api_key=hf_token
) if hf_token else None

# 2. App Configuration & Branding
st.set_page_config(page_title="Dhaka TechMatch", page_icon="🎯", layout="wide")

st.title("🎯 Dhaka TechMatch")
st.caption("AI-Powered Localized Job Skill Matcher for Bangladesh's Tech Ecosystem (Powered by Hugging Face)")
st.markdown("---")

# 3. User Input Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("💼 Target Role & Context")
    target_role = st.text_input(
        "What is your dream job title?", 
        placeholder="e.g., Software Engineer (Backend), Associate Product Manager, DevOps Engineer"
    )
    
    target_company_type = st.selectbox(
        "Target Company Ecosystem in Bangladesh",
        ["Fintech Startups (e.g., bKash, Nagad)", "Ride-Sharing & Logistics (e.g., Pathao, ChalDal)", "Local Software Houses (e.g., TigerIT, Brain Station 23)", "Global Tech Hubs / Remote Hubs"]
    )

with col2:
    st.header("📄 Your Current Profile")
    resume_text = st.text_area(
        "Paste your raw resume text or list your current skill set here:",
        placeholder="Paste text from your CV. Include your university projects, programming languages, and frameworks...",
        height=180
    )

# 4. Processing & Execution Engine
if st.button("🚀 Analyze Skill Gap & Fetch Matching Jobs"):
    if not client:
        st.error("Please supply a valid Hugging Face Token first.")
    elif not target_role or not resume_text:
        st.warning("Please provide both your target job title and your current resume text.")
    else:
        with st.spinner("Scanning local market data (Bdjobs/LinkedIn context) and mapping job openings via Llama-3..."):
            try:
                # Localized prompt instructions
                prompt = f"""
                You are an advanced AI career matching engine specializing in the tech industry of Dhaka, Bangladesh.
                
                Analyze the user's input:
                - Target Role: {target_role}
                - Target Company Type: {target_company_type}
                - Student's Current Resume/Skills: {resume_text}
                
                Generate a comprehensive local tech analysis. Format your response cleanly using Markdown with these exact headers:
                
                ### 🔍 Active Job Openings in Dhaka (Bdjobs & LinkedIn Context)
                List 2 to 3 highly realistic, targeted job openings currently demanded by real companies in Dhaka matching this track (e.g., mention names like bKash, Pathao, Brain Station 23, TigerIT, Selise, ShopUp based on the 'Target Company Type' selected). 
                For each opening, include:
                - **Company Name & Role Title**
                - **Estimated Monthly Salary Range (BDT)** 
                - **Required Tech Stack/Skills mentioned in their typical circulars**
                
                ### 📊 Skill Gap Assessment
                Compare the student's resume against these specific Dhaka job requirements. Bullet-point the exact missing frameworks, libraries, databases, or architectural concepts they need to learn to get hired.
                
                ### 📅 Strict 3-Month Learning Roadmap
                Provide a hyper-focused monthly/weekly breakdown designed to bridge this gap, complete with actionable project ideas relevant to the Dhaka market.
                """
                
                # Request routed directly to Hugging Face
                response = client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3-8B-Instruct",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                
                # Output the response
                st.markdown("---")
                st.success("🎉 Local Job Matching Analysis Complete!")
                st.markdown(response.choices[0].message.content.strip())
                
            except Exception as e:
                st.error(f"An error occurred while connecting with Hugging Face: {e}")
