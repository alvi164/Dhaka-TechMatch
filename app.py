import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load Environment & Initialize Hugging Face Client
load_dotenv()
hf_token = os.getenv("HF_TOKEN")

# App Configuration & Branding
st.set_page_config(page_title="Dhaka TechMatch", page_icon="🎯", layout="wide")

# Custom CSS to style the attribution footer nicely
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: #888888;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #444444;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("⚙️ App Configuration")
    
    # Secure Token Configuration
    if not hf_token:
        st.warning("⚠️ HF_TOKEN not found in secrets.")
        hf_token = st.text_input("Enter Hugging Face Token:", type="password")
    else:
        st.success("🔒 HF_TOKEN loaded from environment.")

    # Model Selection Toggle
    selected_model = st.selectbox(
        "🧠 Select AI Engine",
        [
            "meta-llama/Meta-Llama-3-8B-Instruct",
            "Qwen/Qwen2.5-7B-Instruct"
        ],
        help="Switch engines if one model is running slowly or hitting rate limits."
    )

    st.markdown("---")
    st.header("👨‍💻 Profile Tweaks")
    
    experience_level = st.selectbox(
        "Your Current Career Level",
        ["Student / Fresh Graduate", "Junior Developer (1-2 years)", "Mid-Level Engineer (3+ years)"]
    )

    st.markdown("---")
    # --- CREATOR ATTRIBUTION IN SIDEBAR ---
    st.markdown("### 🛠️ App Creator")
    st.info("**Syad Mehedi Hasan Alvi**\n\n*Connecting local talent with Bangladesh's tech ecosystem.*")

# Initialize Client
client = OpenAI(
    base_url="https://router.huggingface.co/v1/",
    api_key=hf_token
) if hf_token else None


# --- MAIN INTERFACE ---
st.title("🎯 Dhaka TechMatch")
st.caption("AI-Powered Localized Job Skill Matcher for Bangladesh's Tech Ecosystem")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("💼 Target Role & Context")
    target_role = st.text_input(
        "What is your dream job title?", 
        placeholder="e.g., Software Engineer (Backend), Associate Product Manager, DevOps Engineer"
    )
    
    target_company_type = st.selectbox(
        "Target Company Ecosystem in Bangladesh",
        [
            "Fintech Startups (e.g., bKash, Nagad)", 
            "Ride-Sharing & Logistics (e.g., Pathao, ChalDal)", 
            "Local Software Houses (e.g., TigerIT, Brain Station 23)", 
            "Global Tech Hubs / Remote Teams"
        ]
    )

with col2:
    st.header("📄 Your Current Profile")
    resume_text = st.text_area(
        "Paste your raw resume text or list your current skill set here:",
        placeholder="Paste text from your CV. Include your university projects, programming languages, and frameworks...",
        height=180
    )

# --- EXECUTION ENGINE ---
if st.button("🚀 Analyze Skill Gap & Fetch Matching Jobs"):
    if not client:
        st.error("Please supply a valid Hugging Face Token in the sidebar or secrets setup.")
    elif not target_role or not resume_text:
        st.warning("Please provide both your target job title and your current resume text.")
    else:
        with st.spinner(f"Scanning local market data via {selected_model.split('/')[-1]}..."):
            try:
                # Optimized system parameters for targeted results
                prompt = f"""
                You are an advanced AI career matching engine specializing in the tech industry of Dhaka, Bangladesh.
                
                Analyze the user's input:
                - Target Role: {target_role}
                - Experience Level: {experience_level}
                - Target Company Type: {target_company_type}
                - User's Current Resume/Skills: {resume_text}
                
                Generate a comprehensive local tech analysis. Format your response cleanly using Markdown with these exact headers:
                
                ### 🔍 Active Job Openings in Dhaka (Bdjobs & LinkedIn Context)
                List 2 to 3 highly realistic, targeted job openings currently demanded by real companies in Dhaka matching this track (e.g., mention names like bKash, Pathao, Brain Station 23, TigerIT, Selise, ShopUp based on the 'Target Company Type' selected). 
                For each opening, include:
                - **Company Name & Role Title**
                - **Estimated Monthly Salary Range (BDT)** tailored appropriately for a {experience_level}.
                - **Required Tech Stack/Skills mentioned in their typical circulars**
                
                ### 📊 Skill Gap Assessment
                Compare the user's resume against these specific Dhaka job requirements. Bullet-point the exact missing frameworks, libraries, databases, or architectural concepts they need to learn to get hired.
                
                ### 📅 Strict 3-Month Learning Roadmap
                Provide a hyper-focused monthly/weekly breakdown designed to bridge this gap, complete with actionable project ideas relevant to the Dhaka market.
                """
                
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                
                analysis_results = response.choices[0].message.content.strip()
                
                # Output Results
                st.markdown("---")
                st.success("🎉 Local Job Matching Analysis Complete!")
                st.markdown(analysis_results)
                
                # --- NEW UPGRADE: DOWNLOAD BUTTON ---
                st.markdown("---")
                st.download_button(
                    label="💾 Download Roadmap as Markdown File",
                    data=analysis_results,
                    file_name="Dhaka_TechMatch_Roadmap.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"An error occurred while connecting with Hugging Face: {e}")

# --- GLOBAL FOOTER ATTRIBUTION ---
st.markdown(
    '<div class="footer">🚀 Dhaka TechMatch | Designed & Developed by <b>Syad Mehedi Hasan Alvi</b></div>', 
    unsafe_allow_html=True
)
