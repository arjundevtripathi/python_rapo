# app.py
# Complete Developer Portfolio with GenAI & Data Science projects
# Run with: streamlit run app.py

import streamlit as st
import pandas as pd
import base64
from datetime import datetime
import json
import os
from pathlib import Path

# ------------------------------------------------------------------------------
# PAGE CONFIG
st.set_page_config(
    page_title="Arjun | Data Scientist & GenAI Developer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------------------------
# CUSTOM CSS (Glassmorphism, Dark Theme, Animations)
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* Dark background with subtle gradient */
    .stApp {
        background: linear-gradient(135deg, #0b0f1a 0%, #1a1f2e 100%);
        color: #e0e0e0;
    }

    /* Hide Streamlit's default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Glassmorphism card */
    .glass {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .glass:hover {
        transform: translateY(-4px);
        border-color: rgba(100, 200, 255, 0.3);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
    }

    /* Hero section */
    .hero {
        text-align: center;
        padding: 4rem 1rem;
        background: radial-gradient(circle at 30% 30%, rgba(0, 200, 255, 0.08) 0%, transparent 70%);
        border-radius: 30px;
        margin-bottom: 2rem;
    }
    .hero h1 {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6dd5fa, #2980b9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero p {
        font-size: 1.2rem;
        color: #b0b0b0;
        margin: 0.5rem 0;
    }
    .hero .tagline {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin: 1rem 0;
    }
    .hero .tagline span {
        background: rgba(255,255,255,0.05);
        padding: 0.3rem 1.2rem;
        border-radius: 30px;
        font-size: 0.9rem;
        border: 1px solid rgba(255,255,255,0.08);
        color: #c0c0c0;
    }
    .hero .cta-buttons {
        margin-top: 1.5rem;
    }
    .hero .cta-buttons a {
        display: inline-block;
        margin: 0 0.5rem;
        padding: 0.7rem 1.8rem;
        border-radius: 50px;
        background: linear-gradient(135deg, #00c6ff, #0072ff);
        color: #fff;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
    }
    .hero .cta-buttons a:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(0, 114, 255, 0.4);
    }

    /* Stats grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    .stat-item {
        text-align: center;
        background: rgba(255,255,255,0.03);
        padding: 1rem;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .stat-item .number {
        font-size: 2.2rem;
        font-weight: 700;
        color: #6dd5fa;
    }
    .stat-item .label {
        font-size: 0.8rem;
        color: #aaa;
        margin-top: 0.2rem;
    }

    /* Skill bars */
    .skill-bar {
        margin: 0.8rem 0;
    }
    .skill-bar .skill-name {
        display: flex;
        justify-content: space-between;
        font-size: 0.9rem;
    }
    .skill-bar .bar {
        width: 100%;
        height: 8px;
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        margin-top: 4px;
        overflow: hidden;
    }
    .skill-bar .bar .fill {
        height: 100%;
        background: linear-gradient(90deg, #6dd5fa, #2980b9);
        border-radius: 10px;
        transition: width 1s ease;
    }

    /* Project cards grid */
    .project-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    .project-card {
        background: rgba(255,255,255,0.04);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.06);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .project-card:hover {
        transform: translateY(-6px);
        border-color: rgba(100, 200, 255, 0.3);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .project-card .badge {
        display: inline-block;
        background: rgba(0, 200, 255, 0.15);
        color: #6dd5fa;
        font-size: 0.7rem;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        margin-bottom: 0.8rem;
    }
    .project-card h4 {
        margin: 0.5rem 0;
        color: #fff;
    }
    .project-card p {
        font-size: 0.9rem;
        color: #b0b0b0;
        margin: 0.5rem 0;
    }
    .project-card .tech {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin: 0.8rem 0;
    }
    .project-card .tech span {
        background: rgba(255,255,255,0.06);
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.7rem;
        color: #ccc;
    }
    .project-card .btn-link {
        display: inline-block;
        margin-top: 0.8rem;
        padding: 0.4rem 1.2rem;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 30px;
        color: #ddd;
        text-decoration: none;
        font-size: 0.85rem;
        transition: all 0.2s;
    }
    .project-card .btn-link:hover {
        background: rgba(255,255,255,0.1);
        color: #fff;
    }

    /* Blog cards */
    .blog-card {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 1.2rem;
        border-left: 3px solid #6dd5fa;
        margin: 0.8rem 0;
        transition: all 0.2s;
    }
    .blog-card:hover {
        background: rgba(255,255,255,0.06);
        transform: translateX(5px);
    }
    .blog-card h4 {
        margin: 0;
        color: #fff;
    }
    .blog-card .meta {
        font-size: 0.8rem;
        color: #888;
        margin-top: 0.3rem;
    }

    /* Contact section */
    .contact-item {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin: 0.8rem 0;
        padding: 0.6rem 1rem;
        background: rgba(255,255,255,0.03);
        border-radius: 10px;
        transition: all 0.2s;
        text-decoration: none;
        color: #ddd;
    }
    .contact-item:hover {
        background: rgba(255,255,255,0.07);
        color: #fff;
    }
    .contact-item .icon {
        font-size: 1.5rem;
        width: 2rem;
        text-align: center;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .hero h1 { font-size: 2.2rem; }
        .hero .tagline span { font-size: 0.8rem; padding: 0.2rem 0.8rem; }
        .stats-grid { grid-template-columns: repeat(2, 1fr); }
        .project-grid { grid-template-columns: 1fr; }
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #1a1f2e; }
    ::-webkit-scrollbar-thumb { background: #2980b9; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #6dd5fa; }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ------------------------------------------------------------------------------
# DATA
# Skills
skills_data = {
    "Python": 90,
    "Machine Learning": 85,
    "Deep Learning": 80,
    "LLM & GenAI": 88,
    "LangChain": 82,
    "AWS": 75,
    "SQL": 80,
    "Docker": 70,
}

# Statistics
stats = {
    "Experience": "5+ Years",
    "Projects": 30 ,
    "Technologies": 40 ,
    "Certificates": 20 ,
    "GitHub Repos": 100 ,
}

# Portfolio Projects (showcased on Portfolio page)
portfolio_projects = [
    {
        "title": "AI Interview Assistant",
        "description": "Real‑time interview simulator using LLMs and voice.",
        "tech": ["LLM", "LangChain", "Groq", "Streamlit"],
        "link": "#",
        "badge": "🤖 GenAI",
    },
    {
        "title": "PDF Chatbot (RAG)",
        "description": "Chat with your PDF documents using RAG and FAISS.",
        "tech": ["RAG", "FAISS", "OpenAI", "Streamlit"],
        "link": "#",
        "badge": "📄 RAG",
    },
    {
        "title": "Customer Churn Prediction",
        "description": "ML model to predict churn with XGBoost and SHAP.",
        "tech": ["XGBoost", "SHAP", "Scikit‑learn"],
        "link": "#",
        "badge": "📈 ML",
    },
    {
        "title": "Voice Assistant",
        "description": "Speech recognition and LLM‑powered assistant.",
        "tech": ["Whisper", "Groq", "Streamlit"],
        "link": "#",
        "badge": "🎤 Voice",
    },
]

# AI Projects (specific to AI/GenAI)
ai_projects = [
    {"title": "RAG Chatbot", "desc": "Document Q&A with retrieval.", "tech": ["LangChain", "FAISS"]},
    {"title": "Medical Assistant", "desc": "Medical information chatbot.", "tech": ["LLM", "RAG"]},
    {"title": "Resume Analyzer", "desc": "Extract skills and match jobs.", "tech": ["NLP", "OpenAI"]},
    {"title": "SQL Generator", "desc": "Natural language to SQL.", "tech": ["LangChain", "Groq"]},
    {"title": "Multi Agent System", "desc": "Collaborative agents for tasks.", "tech": ["LangGraph", "LangChain"]},
    {"title": "Meeting Summarizer", "desc": "Summarize meeting transcripts.", "tech": ["Whisper", "LLM"]},
]

# ML Projects
ml_projects = [
    {"title": "House Price Prediction", "desc": "Predict house prices with regression.", "tech": ["Scikit‑learn", "Pandas"]},
    {"title": "Fraud Detection", "desc": "Anomaly detection on transactions.", "tech": ["XGBoost", "Imbalanced‑learn"]},
    {"title": "Credit Risk", "desc": "Assess creditworthiness.", "tech": ["Logistic Regression", "SHAP"]},
    {"title": "Recommendation System", "desc": "Collaborative filtering for products.", "tech": ["Surprise", "Pandas"]},
    {"title": "Sales Forecasting", "desc": "Time series forecasting.", "tech": ["Prophet", "Statsmodels"]},
    {"title": "Sentiment Analysis", "desc": "Analyze sentiment in reviews.", "tech": ["NLTK", "Scikit‑learn"]},
]

# Blog posts
blog_posts = [
    {"title": "How RAG Works", "date": "2025-03-10", "summary": "A deep dive into Retrieval Augmented Generation."},
    {"title": "Vector Databases Explained", "date": "2025-02-28", "summary": "Understanding vector search and indexing."},
    {"title": "Prompt Engineering for LLMs", "date": "2025-02-15", "summary": "Best practices and advanced techniques."},
    {"title": "LangChain Tutorial", "date": "2025-02-01", "summary": "Building applications with LangChain."},
    {"title": "Machine Learning Guide", "date": "2025-01-20", "summary": "From data to deployment."},
]

# Certificates
certificates = ["AWS Certified", "Azure AI", "Google Cloud ML", "Python Programming", "TensorFlow Developer", "Deep Learning Specialization", "Generative AI with LLMs"]

# Social links
social_links = {
    "LinkedIn": "https://linkedin.com/in/arjun",
    "GitHub": "https://github.com/arjun",
    "Email": "arjun@example.com",
    "Twitter": "https://twitter.com/arjun",
    "Portfolio": "https://arjun.dev",
    "Resume": "#",
}

# ------------------------------------------------------------------------------
# PAGE FUNCTIONS

def home():
    st.markdown("""
    <div class="hero">
        <h1>👋 Hi, I'm Arjun</h1>
        <p style="font-size:1.3rem;">Data Scientist &nbsp;|&nbsp; AI Engineer &nbsp;|&nbsp; GenAI Developer</p>
        <div class="tagline">
            <span>Python</span> <span>Machine Learning</span> <span>LLM</span>
            <span>RAG</span> <span>LangChain</span> <span>AWS</span>
        </div>
        <div class="cta-buttons">
            <a href="#portfolio">View Portfolio</a>
            <a href="#resume">Download Resume</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Statistics
    cols = st.columns(len(stats))
    for i, (key, value) in enumerate(stats.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="stat-item">
                <div class="number">{value}</div>
                <div class="label">{key}</div>
            </div>
            """, unsafe_allow_html=True)

    # About Me (short)
    with st.container():
        st.markdown("""
        <div class="glass" style="margin-top:2rem;">
            <h3>📌 About Me</h3>
            <p style="color:#c0c0c0;">
            I'm a Data Scientist with 5+ years of experience building <strong>Machine Learning Systems</strong>,
            <strong>Generative AI Applications</strong>, <strong>RAG Systems</strong>, and <strong>LLM-powered tools</strong>.
            I love turning data into products that solve real problems.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Skills
    st.markdown("<h3>⚡ Core Skills</h3>", unsafe_allow_html=True)
    skill_cols = st.columns(2)
    for i, (skill, level) in enumerate(skills_data.items()):
        col = skill_cols[i % 2]
        col.markdown(f"""
        <div class="skill-bar">
            <div class="skill-name"><span>{skill}</span><span>{level}%</span></div>
            <div class="bar"><div class="fill" style="width:{level}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

def about():
    st.markdown("<h2>👨‍💻 About Me</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class="glass">
        <p style="font-size:1.1rem;">
        Hi, I'm <strong>Arjun</strong> – a passionate Data Scientist and Generative AI engineer.
        I hold a Master's degree in Data Science and have worked on projects ranging from predictive
        modeling to cutting‑edge LLM applications.
        </p>
        <p>
        <strong>What I do:</strong><br>
        • Build end‑to‑end machine learning pipelines<br>
        • Develop RAG systems and conversational AI<br>
        • Fine‑tune LLMs for domain‑specific tasks<br>
        • Design scalable cloud architectures (AWS)<br>
        • Automate workflows with Python
        </p>
        <p>
        I believe in <em>learning in public</em> – this portfolio is a reflection of my journey.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3>🎓 Certificates</h3>", unsafe_allow_html=True)
    cert_cols = st.columns(4)
    for i, cert in enumerate(certificates):
        col = cert_cols[i % 4]
        col.markdown(f"✅ {cert}")

def portfolio():
    st.markdown("<h2>💼 Portfolio</h2>", unsafe_allow_html=True)
    st.markdown('<div class="project-grid">', unsafe_allow_html=True)
    for proj in portfolio_projects:
        st.markdown(f"""
        <div class="project-card">
            <div class="badge">{proj['badge']}</div>
            <h4>{proj['title']}</h4>
            <p>{proj['description']}</p>
            <div class="tech">
                {"".join(f"<span>{t}</span>" for t in proj['tech'])}
            </div>
            <a href="{proj['link']}" class="btn-link">View Project →</a>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def ai_projects_page():
    st.markdown("<h2>🤖 AI & GenAI Projects</h2>", unsafe_allow_html=True)
    st.markdown('<div class="project-grid">', unsafe_allow_html=True)
    for proj in ai_projects:
        st.markdown(f"""
        <div class="project-card">
            <h4>{proj['title']}</h4>
            <p>{proj['desc']}</p>
            <div class="tech">{"".join(f"<span>{t}</span>" for t in proj['tech'])}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def ml_projects_page():
    st.markdown("<h2>📊 Data Science & ML Projects</h2>", unsafe_allow_html=True)
    st.markdown('<div class="project-grid">', unsafe_allow_html=True)
    for proj in ml_projects:
        st.markdown(f"""
        <div class="project-card">
            <h4>{proj['title']}</h4>
            <p>{proj['desc']}</p>
            <div class="tech">{"".join(f"<span>{t}</span>" for t in proj['tech'])}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def blog():
    st.markdown("<h2>📝 Blog</h2>", unsafe_allow_html=True)
    for post in blog_posts:
        st.markdown(f"""
        <div class="blog-card">
            <h4>{post['title']}</h4>
            <div class="meta">{post['date']}</div>
            <p>{post['summary']}</p>
        </div>
        """, unsafe_allow_html=True)

def resume():
    st.markdown("<h2>📜 Resume</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class="glass">
        <p>You can download my full resume in PDF format:</p>
        <a href="#" style="display:inline-block;margin-top:0.5rem;padding:0.6rem 1.8rem;background:linear-gradient(135deg,#00c6ff,#0072ff);color:#fff;border-radius:50px;text-decoration:none;font-weight:600;">⬇️ Download Resume (PDF)</a>
    </div>
    """, unsafe_allow_html=True)
    # You can also embed a PDF viewer if you have the file in assets/

def contact():
    st.markdown("<h2>📞 Contact</h2>", unsafe_allow_html=True)
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    for platform, url in social_links.items():
        icon = "🔗" if platform != "Email" else "✉️"
        if platform == "Email":
            display = url
        else:
            display = f"@{platform.lower()}"
        st.markdown(f"""
        <a href="{url}" target="_blank" class="contact-item">
            <span class="icon">{icon}</span>
            <span>{platform}: {display}</span>
        </a>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def learning_hub():
    st.markdown("<h2>📚 Learning Hub</h2>", unsafe_allow_html=True)
    topics = [
        "Python", "NumPy", "Pandas", "Matplotlib", "Statistics",
        "Machine Learning", "Deep Learning", "NLP", "LLM", "RAG",
        "LangChain", "LangGraph", "Vector Database", "Prompt Engineering",
        "MLOps", "AWS", "Docker", "Git"
    ]
    # Display as a grid of tags
    cols = st.columns(4)
    for i, topic in enumerate(topics):
        cols[i % 4].markdown(f"<div style='background:rgba(255,255,255,0.05);padding:0.4rem 0.8rem;border-radius:20px;text-align:center;margin:0.3rem;border:1px solid rgba(255,255,255,0.05);'>{topic}</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# SIDEBAR NAVIGATION (custom, clean)
st.sidebar.markdown("## 🧭 Navigation")
pages = {
    "🏠 Home": home,
    "👨‍💻 About": about,
    "💼 Portfolio": portfolio,
    "🤖 AI Projects": ai_projects_page,
    "📊 ML Projects": ml_projects_page,
    "📚 Learning Hub": learning_hub,
    "📝 Blog": blog,
    "📜 Resume": resume,
    "📞 Contact": contact,
}

# Use radio for navigation
choice = st.sidebar.radio("Go to", list(pages.keys()), index=0)

# Render selected page
pages[choice]()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("© 2025 Arjun | Built with ❤️ using Streamlit")

# ------------------------------------------------------------------------------
# Optional: Add a "Powered by" badge
st.markdown("""
<div style="text-align:center;margin-top:3rem;font-size:0.8rem;color:#555;border-top:1px solid rgba(255,255,255,0.05);padding-top:1rem;">
    <span>🚀 Streamlit Portfolio • Data Scientist • GenAI</span>
</div>
""", unsafe_allow_html=True)