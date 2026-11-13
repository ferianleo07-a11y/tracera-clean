# ==============================================================================
# api_client.py - Klien HTTP Terpusat untuk Komunikasi Backend
# Penanggung Jawab: Orang 4 (Frontend Lead)
# Lokasi: frontend/utils/api_client.py
# ==============================================================================
import os
import requests
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")
INTERNAL_KEY = os.getenv("INTERNAL_API_KEY", "tracera-skills-intelligence-secret-key-2026")

class APIClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.headers = {"X-API-KEY": INTERNAL_KEY}

    @st.cache_data(ttl=300, show_spinner=False)
    def fetch_filter_options(_self):
        """Mengambil daftar dropdown filter dengan caching selama 5 menit."""
        try:
            resp = requests.get(f"{_self.base_url}/analytics/filters", headers=_self.headers, timeout=5)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        return {
            "universities": ["Universitas Gadjah Mada", "Universitas Indonesia", "Institut Teknologi Bandung", "Institut Teknologi Sepuluh Nopember", "Universitas Airlangga", "BINUS University"],
            "study_programs": ["All Study Programs", "Computer Science", "Electrical Engineering", "Industrial Engineering", "Management"],
            "target_roles": ["Software Engineer / Tech Roles", "Data Scientist", "Product Manager", "DevOps Engineer"],
            "industries": ["Technology", "Financial Services", "Consulting", "Consumer Goods", "Telecommunications"],
            "career_levels": ["All", "Entry-Level", "Mid-Senior", "Executive"],
            "locations": ["All", "Indonesia", "Singapore", "Remote"]
            }
    @st.cache_data(ttl=120, show_spinner=False)
    def fetch_dashboard_data(_self, university=None, study_program=None, target_role=None, industry=None):
        """Mengambil seluruh payload data dashboard dari backend FastAPI."""
        params = {}
        if university and university != "All":
            params["university"] = university
        if study_program and study_program not in ["All", "All Study Programs"]:
            params["study_program"] = study_program
        if target_role and target_role not in ["All", "Software Engineer / Tech Roles"]:
            params["target_role"] = target_role
        if industry and industry != "All":
            params["industry"] = industry

        try:
            resp = requests.get(f"{_self.base_url}/analytics/dashboard", params=params, headers=_self.headers, timeout=8)
            if resp.status_code == 200:
                return resp.json(), True
        except Exception:
            pass
        return _self._generate_fallback_data(), False

    @st.cache_data(ttl=120, show_spinner=False)
    def fetch_skills_comparison(_self, universities_list, study_program=None, target_role=None, industry=None):
        """Mengambil data perbandingan multi-universitas dari endpoint backend."""
        unis_param = ",".join(universities_list)
        params = {"universities": unis_param}
        if study_program and study_program not in ["All", "All Study Programs"]:
            params["study_program"] = study_program
        if target_role and target_role not in ["All", "Software Engineer / Tech Roles"]:
            params["target_role"] = target_role
        if industry and industry != "All":
            params["industry"] = industry
            
        try:
            resp = requests.get(f"{_self.base_url}/analytics/skills/comparison", params=params, headers=_self.headers, timeout=8)
            if resp.status_code == 200:
                return resp.json(), True
        except Exception:
            pass
        return _self._generate_fallback_comparison(universities_list), False
    
    def _generate_fallback_data(self):
        return {
            "kpi": {
                "matched_alumni": 240,
                "total_unique_skills": 2850,
                "skill_type_ratio": "72% : 28%",
                "trending_skills_count": 55,
                "mom_growth_str": "+18% MoM",
                "avg_skills_per_profile": 8.1,
                "top_endorsed_skills": 740
            },
            "hard_soft_skills": {
                "hard_skills": [
                    {"rank": 1, "skill_name": "Python Programming", "count": 182, "percentage": 75.8, "endorsements": 740, "demand_badge": "[Demand: ★★★]", "bar_color": "#1d4ed8"},
                    {"rank": 2, "skill_name": "SQL & Relational Databases", "count": 156, "percentage": 65.0, "endorsements": 498, "demand_badge": "[Demand: ★★★]", "bar_color": "#1d4ed8"},
                    {"rank": 3, "skill_name": "Cloud Infrastructure (AWS/GCP)", "count": 112, "percentage": 46.7, "endorsements": 315, "demand_badge": "[Surging ▲]", "bar_color": "#f97316"},
                    {"rank": 4, "skill_name": "System Architecture & Microservices", "count": 98, "percentage": 40.8, "endorsements": 170, "demand_badge": "[Deficit 🔥]", "bar_color": "#ef4444"},
                    {"rank": 5, "skill_name": "Data Structures & Algorithms", "count": 88, "percentage": 36.7, "endorsements": 110, "demand_badge": "[Demand: ★★]", "bar_color": "#1d4ed8"},
                    {"rank": 6, "skill_name": "Docker & Containerization", "count": 76, "percentage": 31.7, "endorsements": 94, "demand_badge": "[Demand: ★★]", "bar_color": "#1d4ed8"}
                ],
                "soft_skills": [
                    {"rank": 1, "skill_name": "Problem Solving & Critical Thinking", "count": 210, "percentage": 87.5, "endorsements": 512, "demand_badge": "[Universal ★★★]", "bar_color":
                    "#10b981"},
                    {"rank": 2, "skill_name": "Cross-functional Collaboration", "count": 178, "percentage": 74.2, "endorsements": 245, "demand_badge": "[High ★★]", "bar_color": "#10b981"},
                    {"rank": 3, "skill_name": "Stakeholder & Client Communication", "count": 134, "percentage": 55.8, "endorsements": 180, "demand_badge": "[Surging ▲]", "bar_color": "#f97316"},
                    {"rank": 4, "skill_name": "Agile & Scrum Coordination", "count": 126, "percentage": 52.5, "endorsements": 165, "demand_badge": "[Standard ★★]", "bar_color": "#10b981"},
                    {"rank": 5, "skill_name": "Adaptability & Continuous Learning", "count": 108, "percentage": 45.0, "endorsements": 140, "demand_badge": "[High ★★]", "bar_color": "#10b981"},
                    {"rank": 6, "skill_name": "Team Leadership & Mentoring", "count": 92, "percentage": 38.3, "endorsements": 125, "demand_badge": "[High ★★]", "bar_color": "#10b981"}
                ]
            },
            "skills_distribution": {
                "categories": [
                    {"category": "Technical & Engineering", "percentage": 61.4, "total": 2850, "subcategories": {"Backend": 1368, "Cloud": 741, "Data": 513, "Other Tech": 228}},
                    {"category": "Soft Skills & Leadership", "percentage": 18.1, "total": 840, "subcategories": {"Communication": 420, "Problem Solving": 268, "Leadership": 152}},
                    {"category": "Business & Product Strategy", "percentage": 11.2, "total": 520, "subcategories": {"Project Mgmt": 302, "Product Owner": 145, "Business Analysis": 73}},
                    {"category": "Tools & Software Platforms", "percentage": 9.3, "total": 430, "subcategories": {"Git / Docker": 224, "Jira / Agile": 129, "CI/CD Tools": 77}}
                ],
                "total_skills_count": 2850
            },
            "skill_network": {
                "nodes": [
                    {"id": "python", "label": "Python", "category": "Tech", "dimension": "Programming Language", "endorsements": 740, "frequency": 182, "pct": 75.8, "size": 34, "color": "#1d4ed8", "x": 0.0, "y": 0.0},
                    {"id": "ds", "label": "Data Science", "category": "Data", "dimension": "Data Analytics", "endorsements": 420, "frequency": 110, "pct": 45.8, "size": 22, "color": "#0d9488", "x": -0.35, "y": 0.28},
                    {"id": "da", "label": "Data Analysis", "category": "Data", "dimension": "Data Analytics", "endorsements": 390, "frequency": 105, "pct": 43.8, "size": 21, "color": "#f97316", "x": 0.42, "y": 0.22},
                    {"id": "sql", "label": "SQL", "category": "Tech", "dimension": "Programming Language", "endorsements": 510, "frequency": 156, "pct": 65.0, "size": 25, "color": "#0284c7",
                    "x": -0.32, "y": -0.22},
                    {"id": "cloud", "label": "Cloud GCP", "category": "Tech", "dimension": "Technical Expertise", "endorsements": 330, "frequency": 112, "pct": 46.7, "size": 19, "color": "#10b981", "x": 0.38, "y": -0.26},
                    {"id": "tableau", "label": "Tableau", "category": "Data", "dimension": "Data Analytics", "endorsements": 260, "frequency": 75, "pct": 31.2, "size": 15, "color": "#f97316",
                    "x": 0.65, "y": 0.35},
                    {"id": "pm", "label": "Project Mgmt", "category": "Business", "dimension": "Strategic Thinking", "endorsements": 310, "frequency": 85, "pct": 35.4, "size": 18, "color": "#7c3aed", "x": 0.0, "y": -0.42},
                    {"id": "scrum", "label": "Scrum", "category": "Business", "dimension": "Strategic Thinking", "endorsements": 220, "frequency": 60, "pct": 25.0, "size": 14, "color": "#a855f7", "x": -0.16, "y": -0.62}
                ],
                "edges": [
                    {"source": "python", "target": "ds", "weight": 4.5},
                    {"source": "python", "target": "da", "weight": 4.0},
                    {"source": "python", "target": "sql", "weight": 5.0},
                    {"source": "python", "target": "cloud", "weight": 3.8},
                    {"source": "da", "target": "tableau", "weight": 3.2},
                    {"source": "pm", "target": "scrum", "weight": 4.2},
                    {"source": "python", "target": "pm", "weight": 2.5}
                ],
                "central_hub": "Python"
            },
            "trending_gap": {
                "items": [
                    {"no": "01", "skill_name": "Python Programming", "skill_type": "Hard Skill", "alumni_count": 182, "alumni_pct": 75.8, "trend_30d_pct": 100.0, "market_demand_pct": 90.0, "gap_score": -14.2, "gap_status": "Significant Talent Gap", "target_roles": ["Software Engineer", "Data Scientist"]},
                    {"no": "02", "skill_name": "System Architecture & Microservices", "skill_type": "Hard Skill", "alumni_count": 98, "alumni_pct": 40.8, "trend_30d_pct": 87.5, "market_demand_pct": 62.3, "gap_score": -21.5, "gap_status": "Critical Deficit / Highest Shortage", "target_roles": ["Tech Lead", "Senior Backend"]},
                    {"no": "03", "skill_name": "Problem Solving & Critical Thinking", "skill_type": "Soft Skill", "alumni_count": 210, "alumni_pct": 87.5, "trend_30d_pct": 48.9, "market_demand_pct": 83.7, "gap_score": 3.8, "gap_status": "Safe & Balanced Supply", "target_roles": ["Full Stack", "Product Manager"]},
                    {"no": "04", "skill_name": "Cloud Infrastructure (AWS/GCP)", "skill_type": "Tools & Infra", "alumni_count": 112, "alumni_pct": 46.7, "trend_30d_pct": 100.0, "market_demand_pct": 64.7, "gap_score": -18.0, "gap_status": "Significant Talent Gap", "target_roles": ["DevOps Engineer", "Cloud Architect"]},
                    {"no": "05", "skill_name": "Cross-functional Stakeholder Management", "skill_type": "Soft Skill", "alumni_count": 134, "alumni_pct": 55.8, "trend_30d_pct": 72.4, "market_demand_pct": 62.3, "gap_score": -6.5, "gap_status": "Moderate Demand Gap", "target_roles": ["Product Owner", "Tech Consultant"]}
                ],
                "total_job_postings_analyzed": 1200,
                "summary_insights": {
                    "hub": "Python is the primary connectivity hub (centrality 0.88), bridging Data Science, Backend API, and DevOps.",
                    "dominance": "Technical & Engineering accounts for 61.4% of total alumni skills, dominated by Backend engineering.",
                    "gap": "System Architecture exhibits the largest deficit (-21.5%), required by 62% of recruitments but held by only 40.8% of alumni.",
                    "coverage": "Analysis extracted from 240 verified alumni profiles matched against active industry market benchmarks.",
                    "rank_combo": "Python + SQL + Problem Solving is held by 71.4% of alumni who advanced to Senior roles within 3 years.",
                    "rank_accel": "Cloud Infrastructure and API Design show +100% adoption velocity in recent alumni profiles over the last 30 days."
                }
            }
        }
    def _generate_fallback_comparison(self, universities_list):
        return {
            "selected_universities": universities_list,
            "comparison_cards": [
                {
                    "university_name": "Universitas Gadjah Mada",
                    "micro_summary": {"matched_alumni": 51, "skill_type_ratio": "72% : 28%", "market_alignment_pct": 76.4, "market_alignment_label": "Leader", "highest_velocity_skill": "CloudInfra (+35%)"},
                    "top_hard_skills": [
                        {"rank": 1, "skill_name": "Python Programming", "count": 39, "percentage": 76.5, "demand_badge": "Safe", "badge_type": "safe"},
                        {"rank": 2, "skill_name": "SQL & Relational DB", "count": 33, "percentage": 64.7, "demand_badge": "High Demand", "badge_type": "demand"},
                        {"rank": 3, "skill_name": "Cloud Infrastructure", "count": 24, "percentage": 47.1, "demand_badge": "Emerging Gap", "badge_type": "gap"},
                        {"rank": 4, "skill_name": "System Architecture", "count": 21, "percentage": 41.2, "demand_badge": "Critical Deficit", "badge_type": "deficit"},
                        {"rank": 5, "skill_name": "Data Structures", "count": 19, "percentage": 37.3, "demand_badge": "High Demand", "badge_type": "demand"}
                    ],
                    "top_soft_skills": [
                        {"rank": 1, "skill_name": "Problem Solving", "count": 44, "percentage": 86.3, "demand_badge": "Soft Skill", "badge_type": "soft"},
                        {"rank": 2, "skill_name": "Cross-functional Collab.", "count": 38, "percentage": 74.5, "demand_badge": "Soft Skill", "badge_type": "soft"},
                        {"rank": 3, "skill_name": "Agile & Scrum Coord.", "count": 27, "percentage": 52.9, "demand_badge": "Soft Skill", "badge_type": "soft"},
                        {"rank": 4, "skill_name": "Stakeholder Comm.", "count": 26, "percentage": 51.0, "demand_badge": "Soft Skill", "badge_type": "soft"}
                    ],
                    "signature_skills": [
                        {"skill_name": "Cloud Infrastructure & Microservices", "diff_pct": "+14% vs benchmark"},
                        {"skill_name": "Python Automation Pipelines", "diff_pct": "+11% vs benchmark"}
                    ]
                },
                {
                    "university_name": "Universitas Indonesia",
                    "micro_summary": {"matched_alumni": 36, "skill_type_ratio": "68% : 32%", "market_alignment_pct": 68.2, "market_alignment_label": "Moderate", "highest_velocity_skill": "Python (+22%)"},
                    "top_hard_skills": [
                        {"rank": 1, "skill_name": "SQL & Relational DB", "count": 26, "percentage": 72.2, "demand_badge": "Safe", "badge_type": "safe"},
                        {"rank": 2, "skill_name": "Python Programming", "count": 23, "percentage": 63.9, "demand_badge": "High Demand", "badge_type": "demand"},
                        {"rank": 3, "skill_name": "Data Structures & Alg.", "count": 17, "percentage": 47.2, "demand_badge": "High Demand", "badge_type": "demand"},
                        {"rank": 4, "skill_name": "Cloud Infrastructure", "count": 14, "percentage": 38.9, "demand_badge": "Emerging Gap", "badge_type": "gap"},
                        {"rank": 5, "skill_name": "System Architecture", "count": 11, "percentage": 30.6, "demand_badge": "Critical Deficit", "badge_type": "deficit"}
                    ],
                    "top_soft_skills": [
                        {"rank": 1, "skill_name": "Cross-functional Collab.", "count": 29, "percentage": 80.6, "demand_badge": "Soft Skill", "badge_type": "soft"},
                        {"rank": 2, "skill_name": "Problem Solving", "count": 28, "percentage": 77.8, "demand_badge": "Soft Skill", "badge_type": "soft"},
                        {"rank": 3, "skill_name": "Stakeholder Comm.", "count": 21, "percentage": 58.3, "demand_badge": "Soft Skill", "badge_type": "soft"},
                        {"rank": 4, "skill_name": "Agile & Scrum Coord.", "count": 17, "percentage": 47.2, "demand_badge": "Soft Skill", "badge_type": "soft"}
                    ],
                    "signature_skills": [
                        {"skill_name": "Product Analytics & Strategy", "diff_pct": "+16% vs benchmark"},
                        {"skill_name": "SQL Database Optimization", "diff_pct": "+9% vs benchmark"}
                    ]
                },
                {
                    "university_name": "Institut Teknologi Bandung",
                    "micro_summary": {"matched_alumni": 39, "skill_type_ratio": "75% : 25%", "market_alignment_pct": 74.8, "market_alignment_label": "High", "highest_velocity_skill": "Docker/K8s (+31%)"},
                    "top_hard_skills": [
                        {"rank": 1, "skill_name": "Python Programming", "count": 27, "percentage": 69.2, "demand_badge": "Safe", "badge_type": "safe"},
                        {"rank": 2, "skill_name": "Docker & Containerization", "count": 23, "percentage": 59.0, "demand_badge": "Safe", "badge_type": "safe"},
                        {"rank": 3, "skill_name": "System Architecture", "count": 20, "percentage": 51.3, "demand_badge": "Emerging Gap", "badge_type": "gap"},
                        {"rank": 4, "skill_name": "Distributed Systems", "count": 18, "percentage": 46.2, "demand_badge": "High Demand", "badge_type": "demand"},
                        {"rank": 5, "skill_name": "Cloud Infrastructure", "count": 17, "percentage": 43.6, "demand_badge": "Emerging Gap", "badge_type": "gap"}
                    ],
                    "top_soft_skills": [
                        {"rank": 1, "skill_name": "Problem Solving", "count": 33, "percentage": 84.6, "demand_badge": "Soft Skill", "badge_type": "soft"},
                        {"rank": 2, "skill_name": "Cross-functional Collab.", "count": 26, "percentage": 66.7, "demand_badge": "Soft Skill", "badge_type": "soft"},
                        {"rank": 3, "skill_name": "Agile & Scrum Coord.", "count": 22, "percentage": 56.4, "demand_badge": "Soft Skill", "badge_type": "soft"},
                        {"rank": 4, "skill_name": "Technical Mentorship", "count": 19, "percentage": 48.7, "demand_badge": "Soft Skill", "badge_type": "soft"}
                    ],
                    "signature_skills": [
                        {"skill_name": "Distributed Systems Architecture", "diff_pct": "+19% vs benchmark"},
                        {"skill_name": "Docker & K8s Pipelines", "diff_pct": "+15% vs benchmark"}
                    ]
                }
            ],
            "executive_takeaways": [
                {"title": "Strongest Technical Pipeline", "description": "ITB demonstrates solid leadership in core infrastructure, systems architecture, and containerization.", "card_type":
                "default"},
                {"title": "Shared Critical Gap", "description": "System Architecture & Cloud Security average below 45% across all selected universities, indicating an industry-wide talent gap.", "card_type": "critical"},
                {"title": "Highest Skill Diversity", "description": "UGM leads in diverse modern tool adoption, data engineering pipelines, and backend stacks.", "card_type": "default"},
                {"title": "Fastest Growing Skill", "description": "Docker & Kubernetes pipelines record the highest adoption velocity (+85%) over the last 30 days among recent graduates.", "card_type": "success"}
            ]
        }
    
api_client = APIClient()