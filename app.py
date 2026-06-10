import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load Environment & Initialize OpenAI Client
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.warning("⚠️ OPENAI_API_KEY not found in .env file. Please enter it below to run the app:")
    api_key = st.text_input("Enter OpenAI API Key:", type="password")

client = OpenAI(api_key=api_key) if api_key else None

# 2. App Configuration & Branding
st.set_page_config(page_title="Dhaka TechMatch", page_icon="🎯", layout="wide")

st.title("🎯 Dhaka TechMatch")
st.caption("AI-Powered Localized Job Skill Matcher for Bangladesh's Tech Ecosystem")
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
if st.button("🚀 Analyze Skill Gap & Generate 3-Month Roadmap"):
    if not client:
        st.error("Please supply a valid OpenAI API Key first.")
    elif not target_role or not resume_text:
        st.warning("Please provide both your target job title and your current resume text.")
    else:
        with st.spinner("Analyzing current Dhaka tech market trends and benchmarking your resume..."):
            try:
                # Prompt constructed to explicitly handle localized market context
                prompt = f"""
                You are an expert tech recruiter and engineering mentor specializing in the tech industry of Dhaka, Bangladesh.
                
                Analyze the following user data:
                - Target Role: {target_role}
                - Target Company Type: {target_company_type}
                - Student's Current Resume/Skills: {resume_text}
                
                Based on current market demands (similar to what is frequently posted on Bdjobs and LinkedIn for Dhaka tech firms like bKash, Pathao, Brain Station 23, etc.), generate a highly detailed analysis.
                
                Format your response cleanly using Markdown with the following exact headers:
                
                ### 📊 Skill Gap Assessment
                Identify which key languages, tools, frameworks, and architectural concepts are missing from the student's resume that are mandatory for this role in the Dhaka ecosystem.
                
                ### 🛠️ Local Market Realities
                Provide a quick 2-3 sentence overview of what tech stack trends are currently driving {target_company_type} in Bangladesh right now regarding this role.
                
                ### 📅 Strict 3-Month Learning Roadmap
                Break down a hyper-focused, week-by-week or month-by-month study plan over 3 months to close this specific gap. Be highly precise with suggested action items, free resources, or project paradigms to build.
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                
                # Output the markdown response cleanly
                st.markdown("---")
                st.success("🎉 Analysis Complete! Your personalized local roadmap is ready below:")
                st.markdown(response.choices[0].message.content.strip())
                
            except Exception as e:
                st.error(f"An error occurred while connecting with OpenAI: {e}")
