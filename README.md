# 🎯 Dhaka TechMatch

**Dhaka TechMatch** is a professional Streamlit career-intelligence app for Bangladesh's tech ecosystem. It helps students, junior engineers, and working professionals compare their current resume against market expectations, identify missing skills, and build a practical 90-day hiring roadmap.

## ✨ What's included

- **Industry-ready UI** with a polished dashboard, responsive layout, sidebar workspace, and tabbed reporting.
- **Local fit engine** that benchmarks a pasted resume against role-specific skill blueprints.
- **Dhaka-market opportunity simulation** for fintech, logistics, software houses, startups, and remote teams.
- **Skill-gap analytics** showing matched skills, missing skills, and a percentage market-fit score.
- **90-day action roadmap** with monthly execution plans and portfolio project suggestions.
- **Optional AI recruiter report** through the Hugging Face OpenAI-compatible router when `HF_TOKEN` is available.
- **Export tools** for JSON career reports and Markdown roadmaps.

## 🧠 Supported role blueprints

- Backend Engineer
- Frontend Engineer
- Full-Stack Engineer
- DevOps / Cloud Engineer
- Data / ML Engineer
- Product / QA Engineer

## 🛠️ Tech stack

- **App framework:** Streamlit
- **AI gateway:** Hugging Face router through the OpenAI Python SDK
- **Secrets:** `python-dotenv` and Streamlit secrets
- **Language:** Python 3.10+
- **Theme:** Streamlit theme settings in `.streamlit/config.toml`

## 🚀 Quick start

```bash
git clone https://github.com/alvi164/Dhaka-TechMatch.git
cd Dhaka-TechMatch
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## 🔐 Optional AI setup

The app works without AI by using the built-in local fit engine. For recruiter-style generated reports, add a Hugging Face token:

```bash
export HF_TOKEN="your_hugging_face_token"
streamlit run app.py
```

Or copy `.env.example` to `.env`, or create `.streamlit/secrets.toml`:

```toml
HF_TOKEN = "your_hugging_face_token"
```

## 📦 Exports

After generating a report, use the **Export** tab to download:

- `dhaka-techmatch-report.json`
- `dhaka-techmatch-roadmap.md`

## ✅ Production-readiness notes

- Keep secrets out of Git and environment-specific config.
- Validate live job postings before applying; market snapshots are planning simulations.
- Add automated tests before extending the app with persistence, authentication, or live job integrations.
- Prefer clear portfolio evidence: deployed apps, GitHub READMEs, diagrams, tests, and measurable outcomes.

## 👤 Creator

Designed and developed by **Syad Mehedi Hasan Alvi**.
