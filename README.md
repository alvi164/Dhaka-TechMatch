# 🎯 Dhaka TechMatch

> **AI-Powered Localized Job Skill Matcher for Bangladesh's Tech Ecosystem**

Dhaka TechMatch is an intelligent career-matching application designed explicitly to bridge the gap between academic theory taught in universities and the rapid, stack-specific requirements of Bangladesh's modern tech ecosystem.

## 💡 The Problem
Many university graduates in Dhaka possess strong theoretical foundations but lack the specific framework and infrastructure experience (e.g., React.js, Spring Boot, Docker, CI/CD) actively sought by top local employers on platforms like Bdjobs and LinkedIn.

## 🚀 Key Features
- **Real-World Market Alignment**: Simulates current job market demands for the Dhaka ecosystem, targeting specific verticals like Fintech (bKash, Nagad), Ride-Sharing (Pathao), and Local Software Houses (Brain Station 23, TigerIT).
- **Active Job Opening Generation**: Automatically generates realistic, locally relevant job openings complete with estimated salary ranges (BDT) and required tech stacks.
- **Automated Resume Benchmarking**: Leverages the OpenAI API to perform a fast semantic audit of pasteable resume profiles against localized industry standards.
- **Strict 3-Month Action Roadmap**: Generates a hyper-focused, week-by-week learning plan designed to make the applicant highly hireable within 90 days.

## 🛠️ Architecture Stack
- **Frontend & Routing**: Streamlit (Python Native Reactive Web App Architecture)
- **Intelligence Gateway**: OpenAI API Engine (`gpt-4o-mini`)
- **Environment Management**: `python-dotenv` for secure credential handling

## 🏁 Quick Start Guide

**1. Clone the isolated repository:**
```bash
git clone [https://github.com/alvi164/Dhaka-TechMatch.git](https://github.com/alvi164/Dhaka-TechMatch.git)
cd Dhaka-TechMatch
