import json
import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

APP_NAME = "Dhaka TechMatch"
APP_TAGLINE = "Industry-ready career intelligence for Bangladesh's tech ecosystem"
CREATOR = "Syad Mehedi Hasan Alvi"
HF_ROUTER_URL = "https://router.huggingface.co/v1/"
DEFAULT_MODELS = [
    "meta-llama/Meta-Llama-3-8B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
]

ROLE_BLUEPRINTS = {
    "Backend Engineer": {
        "skills": ["python", "java", "node.js", "django", "fastapi", "spring boot", "postgresql", "redis", "docker", "rest api", "microservices"],
        "projects": ["Payment ledger API", "Role-based admin dashboard", "Queue-backed notification service"],
        "companies": ["bKash", "Nagad", "ShopUp", "Brain Station 23"],
    },
    "Frontend Engineer": {
        "skills": ["javascript", "typescript", "react", "next.js", "redux", "tailwind", "html", "css", "api integration", "testing"],
        "projects": ["Fintech onboarding flow", "Marketplace product dashboard", "Analytics-heavy admin portal"],
        "companies": ["Pathao", "Chaldal", "10 Minute School", "Sheba Platform"],
    },
    "Full-Stack Engineer": {
        "skills": ["javascript", "typescript", "react", "node.js", "python", "postgresql", "docker", "rest api", "authentication", "cloud"],
        "projects": ["SaaS subscription app", "Courier tracking platform", "Multi-tenant CRM"],
        "companies": ["Selise", "TigerIT", "BJIT", "Kaz Software"],
    },
    "DevOps / Cloud Engineer": {
        "skills": ["linux", "docker", "kubernetes", "aws", "ci/cd", "terraform", "nginx", "monitoring", "bash", "security"],
        "projects": ["Blue-green deployment pipeline", "Kubernetes monitoring stack", "Secure cloud landing zone"],
        "companies": ["DataSoft", "SSL Wireless", "Brain Station 23", "Remote-first teams"],
    },
    "Data / ML Engineer": {
        "skills": ["python", "sql", "pandas", "scikit-learn", "machine learning", "etl", "airflow", "postgresql", "dashboard", "statistics"],
        "projects": ["Customer churn model", "Job-market skill dashboard", "ETL pipeline for transaction analytics"],
        "companies": ["bKash", "ShopUp", "iFarmer", "Arogga"],
    },
    "Product / QA Engineer": {
        "skills": ["agile", "jira", "test cases", "api testing", "postman", "automation", "selenium", "analytics", "documentation", "communication"],
        "projects": ["Regression suite for mobile wallet", "Product requirement document", "Bug triage dashboard"],
        "companies": ["Pathao", "Chaldal", "TigerIT", "Therap Services"],
    },
}

COMPANY_ECOSYSTEMS = [
    "Fintech Startups (bKash, Nagad, Upay)",
    "Ride-Sharing & Logistics (Pathao, Chaldal, Paperfly)",
    "Local Software Houses (TigerIT, Brain Station 23, Kaz Software)",
    "EdTech / HealthTech / Impact Startups",
    "Global Tech Hubs / Remote Teams",
]

LEARNING_RESOURCES = {
    "Backend": ["Build APIs with authentication", "Learn SQL indexing and transactions", "Practice Dockerized deployments"],
    "Frontend": ["Ship React/Next.js portfolio projects", "Add testing and accessibility checks", "Practice API state management"],
    "DevOps": ["Automate CI/CD", "Deploy to a cloud VM", "Add logs, metrics, and alerts"],
    "Data": ["Create reproducible notebooks", "Build ETL pipelines", "Publish dashboards with business insights"],
}


st.set_page_config(page_title=APP_NAME, page_icon="🎯", layout="wide", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
        .stApp {background: linear-gradient(135deg, #07111f 0%, #0d1b2a 45%, #102a43 100%);}
        .hero-card {padding: 2rem; border-radius: 1.2rem; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.16); box-shadow: 0 20px 60px rgba(0,0,0,0.25);}
        .metric-card {padding: 1rem; border-radius: 1rem; background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.12); min-height: 135px;}
        .section-card {padding: 1.2rem; border-radius: 1rem; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.10); margin-bottom: 1rem;}
        .small-muted {color: #b8c7d9; font-size: 0.95rem;}
        .footer {position: fixed; left: 0; bottom: 0; width: 100%; background: rgba(7,17,31,0.86); color: #b8c7d9; text-align: center; padding: 8px; font-size: 13px; border-top: 1px solid rgba(255,255,255,0.12); z-index: 99;}
        div[data-testid="stMetricValue"] {font-size: 2rem;}
    </style>
    """,
    unsafe_allow_html=True,
)


def normalize(text):
    return (text or "").lower().replace("nodejs", "node.js").replace("nextjs", "next.js")


def infer_role_blueprint(target_role):
    normalized = normalize(target_role)
    if any(word in normalized for word in ["front", "react", "ui", "web"]):
        return "Frontend Engineer"
    if any(word in normalized for word in ["full", "mern", "stack"]):
        return "Full-Stack Engineer"
    if any(word in normalized for word in ["devops", "cloud", "sre", "platform"]):
        return "DevOps / Cloud Engineer"
    if any(word in normalized for word in ["data", "ml", "ai", "machine"]):
        return "Data / ML Engineer"
    if any(word in normalized for word in ["product", "qa", "test"]):
        return "Product / QA Engineer"
    return "Backend Engineer"


def calculate_fit_score(resume_text, required_skills):
    profile = normalize(resume_text)
    matched = [skill for skill in required_skills if skill in profile]
    missing = [skill for skill in required_skills if skill not in profile]
    score = round((len(matched) / max(len(required_skills), 1)) * 100)
    return score, matched, missing


def build_market_snapshot(role_key, ecosystem, experience_level):
    blueprint = ROLE_BLUEPRINTS[role_key]
    level_multiplier = {
        "Student / Fresh Graduate": (25000, 45000),
        "Junior Developer (1-2 years)": (45000, 80000),
        "Mid-Level Engineer (3+ years)": (80000, 150000),
        "Senior / Lead (5+ years)": (150000, 280000),
    }[experience_level]
    openings = []
    for index, company in enumerate(blueprint["companies"][:3], start=1):
        openings.append(
            {
                "rank": index,
                "company": company,
                "role": f"{role_key} - {ecosystem.split('(')[0].strip()}",
                "salary": f"BDT {level_multiplier[0]:,} - {level_multiplier[1]:,}/month",
                "skills": ", ".join(blueprint["skills"][:6 + index]),
            }
        )
    return openings


def build_roadmap(missing_skills, role_key):
    primary_gaps = missing_skills[:9] or ["portfolio polish", "interview practice", "system design basics"]
    projects = ROLE_BLUEPRINTS[role_key]["projects"]
    return {
        "Month 1 - Foundation": [
            f"Close fundamentals gaps: {', '.join(primary_gaps[:3])}.",
            "Refresh GitHub profile, README writing, and deployment workflow.",
            f"Mini project: {projects[0]} with clean commits and API documentation.",
        ],
        "Month 2 - Production Skills": [
            f"Practice advanced topics: {', '.join(primary_gaps[3:6] or primary_gaps[:3])}.",
            "Add tests, logging, validation, and security-minded defaults.",
            f"Portfolio project: {projects[1]} with CI-ready structure.",
        ],
        "Month 3 - Hiring Sprint": [
            f"Target final gaps: {', '.join(primary_gaps[6:9] or primary_gaps[:3])}.",
            "Prepare STAR stories, mock interviews, and localized salary expectations.",
            f"Capstone: {projects[2]} deployed with a short technical case study.",
        ],
    }


def load_hf_token():
    token = os.getenv("HF_TOKEN")
    if token:
        return token
    try:
        return st.secrets.get("HF_TOKEN", None)
    except Exception:
        return None


def get_client(hf_token):
    if not hf_token:
        return None
    return OpenAI(base_url=HF_ROUTER_URL, api_key=hf_token)


def build_ai_prompt(target_role, experience_level, ecosystem, resume_text, fit_score, missing_skills):
    return f"""
You are a senior Bangladesh tech recruiter and career coach. Produce a concise, practical, industry-ready report.

Candidate target role: {target_role}
Experience level: {experience_level}
Target company ecosystem: {ecosystem}
Current profile/resume: {resume_text}
Local fit score from rule engine: {fit_score}%
Detected missing skills: {', '.join(missing_skills) if missing_skills else 'No major gaps detected'}

Use Markdown with these exact sections:
### Executive Hiring Verdict
### Dhaka Market-Matched Openings
### Skill Gap Assessment
### Portfolio Projects To Build
### 30-60-90 Day Roadmap
### Interview Preparation Checklist

Be realistic about Bangladesh hiring standards, salary expectations, portfolio evidence, and recruiter screening.
"""


def render_openings(openings):
    for opening in openings:
        st.markdown(
            f"""
            <div class="section-card">
                <strong>#{opening['rank']} {opening['company']} — {opening['role']}</strong><br>
                <span class="small-muted">Estimated range: {opening['salary']}</span><br><br>
                <strong>Typical stack:</strong> {opening['skills']}
            </div>
            """,
            unsafe_allow_html=True,
        )


with st.sidebar:
    st.header("⚙️ Workspace")
    hf_token = load_hf_token()
    if not hf_token:
        st.warning("HF_TOKEN was not found. You can still use the local fit engine.")
        hf_token = st.text_input("Optional Hugging Face token", type="password")
    else:
        st.success("Secure AI token loaded.")

    selected_model = st.selectbox("AI engine", DEFAULT_MODELS, help="Used only when an HF token is available.")
    experience_level = st.selectbox(
        "Career level",
        ["Student / Fresh Graduate", "Junior Developer (1-2 years)", "Mid-Level Engineer (3+ years)", "Senior / Lead (5+ years)"],
    )
    use_ai = st.toggle("Generate recruiter-grade AI report", value=bool(hf_token), disabled=not bool(hf_token))
    st.markdown("---")
    st.info(f"Built by **{CREATOR}** for Bangladesh-focused tech career planning.")

st.markdown(
    f"""
    <div class="hero-card">
        <h1>🎯 {APP_NAME}</h1>
        <p class="small-muted">{APP_TAGLINE}</p>
        <p>Benchmark a resume against local hiring expectations, discover missing skills, and generate a practical 90-day plan for Dhaka's competitive tech market.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")
input_col, context_col = st.columns([1.1, 0.9])
with input_col:
    target_role = st.text_input("Target role", placeholder="e.g., Backend Engineer, React Developer, DevOps Engineer")
    resume_text = st.text_area(
        "Resume / skills / project summary",
        placeholder="Paste your CV text, skills, projects, internship work, GitHub highlights, and tools you have used...",
        height=230,
    )
with context_col:
    ecosystem = st.selectbox("Target company ecosystem", COMPANY_ECOSYSTEMS)
    portfolio_link = st.text_input("Portfolio or GitHub link (optional)", placeholder="https://github.com/your-name")
    interview_goal = st.radio("Primary goal", ["First job", "Better salary", "Remote role", "Leadership track"], horizontal=True)
    st.caption("Tip: Include projects, metrics, and deployment links for a stronger fit score.")

submitted = st.button("🚀 Generate Industry-Ready Career Report", type="primary", use_container_width=True)

if submitted:
    if not target_role.strip() or not resume_text.strip():
        st.warning("Please provide both a target role and your current resume/profile text.")
    else:
        role_key = infer_role_blueprint(target_role)
        required_skills = ROLE_BLUEPRINTS[role_key]["skills"]
        fit_score, matched_skills, missing_skills = calculate_fit_score(resume_text, required_skills)
        openings = build_market_snapshot(role_key, ecosystem, experience_level)
        roadmap = build_roadmap(missing_skills, role_key)
        report_payload = {
            "generated_at_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "target_role": target_role,
            "role_blueprint": role_key,
            "experience_level": experience_level,
            "target_ecosystem": ecosystem,
            "primary_goal": interview_goal,
            "portfolio_link": portfolio_link,
            "fit_score": fit_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "openings": openings,
            "roadmap": roadmap,
        }

        st.session_state["latest_report"] = report_payload
        st.success("Career intelligence report generated.")

        metric_one, metric_two, metric_three, metric_four = st.columns(4)
        metric_one.metric("Market fit", f"{fit_score}%")
        metric_two.metric("Matched skills", len(matched_skills))
        metric_three.metric("Priority gaps", len(missing_skills))
        metric_four.metric("Role blueprint", role_key.split()[0])

        tab_overview, tab_market, tab_roadmap, tab_ai, tab_export = st.tabs(
            ["📊 Overview", "🏢 Market", "📅 Roadmap", "🤖 AI Recruiter", "⬇️ Export"]
        )

        with tab_overview:
            left, right = st.columns(2)
            with left:
                st.subheader("Skills already visible")
                if matched_skills:
                    st.success(", ".join(matched_skills))
                else:
                    st.error("No required skills were clearly detected. Add concrete technologies and project outcomes to your resume.")
            with right:
                st.subheader("Priority skill gaps")
                if missing_skills:
                    st.warning(", ".join(missing_skills))
                else:
                    st.success("Your resume covers the core blueprint. Focus on proof, metrics, and interview depth.")
            st.progress(fit_score / 100)
            st.subheader("Industry-readiness checklist")
            checklist = [
                "Resume has measurable project outcomes",
                "GitHub contains pinned, documented projects",
                "At least one deployed production-style app exists",
                "Can explain database, API, and security decisions",
                "Prepared salary expectations for Bangladesh market",
            ]
            for item in checklist:
                st.checkbox(item, value=False, key=f"check_{item}")

        with tab_market:
            st.subheader("Dhaka-market matched opportunities")
            render_openings(openings)
            st.caption("These are realistic market simulations for planning; verify live openings on Bdjobs, LinkedIn, company career pages, and community groups before applying.")

        with tab_roadmap:
            st.subheader("90-day execution roadmap")
            for month, actions in roadmap.items():
                with st.expander(month, expanded=True):
                    for action in actions:
                        st.write(f"- {action}")
            st.subheader("Suggested learning focus")
            for category, resources in LEARNING_RESOURCES.items():
                with st.expander(category):
                    for resource in resources:
                        st.write(f"- {resource}")

        with tab_ai:
            if use_ai and hf_token:
                with st.spinner(f"Generating recruiter-grade analysis with {selected_model.split('/')[-1]}..."):
                    client = get_client(hf_token)
                    prompt = build_ai_prompt(target_role, experience_level, ecosystem, resume_text, fit_score, missing_skills)
                    try:
                        response = client.chat.completions.create(
                            model=selected_model,
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.55,
                        )
                        ai_report = response.choices[0].message.content.strip()
                        st.session_state["latest_ai_report"] = ai_report
                        st.markdown(ai_report)
                    except Exception as error:
                        st.error(f"AI report generation failed: {error}")
                        st.info("The local report is still available in the other tabs and export section.")
            else:
                st.info("Add an HF_TOKEN in Streamlit secrets or the sidebar to generate the AI recruiter report.")

        with tab_export:
            json_report = json.dumps(report_payload, indent=2, ensure_ascii=False)
            markdown_report = f"""# {APP_NAME} Career Report

Generated: {report_payload['generated_at_utc']}

## Candidate Goal
- Target role: {target_role}
- Blueprint: {role_key}
- Ecosystem: {ecosystem}
- Experience: {experience_level}
- Goal: {interview_goal}
- Portfolio: {portfolio_link or 'Not provided'}

## Fit Score
{fit_score}%

## Matched Skills
{', '.join(matched_skills) if matched_skills else 'None detected'}

## Missing Skills
{', '.join(missing_skills) if missing_skills else 'No major gaps detected'}

## Roadmap
"""
            for month, actions in roadmap.items():
                markdown_report += f"\n### {month}\n" + "\n".join([f"- {action}" for action in actions]) + "\n"
            st.download_button("Download JSON report", json_report, "dhaka-techmatch-report.json", "application/json")
            st.download_button("Download Markdown roadmap", markdown_report, "dhaka-techmatch-roadmap.md", "text/markdown")

st.markdown(
    f'<div class="footer">🚀 {APP_NAME} | Designed & Developed by <b>{CREATOR}</b></div>',
    unsafe_allow_html=True,
)
