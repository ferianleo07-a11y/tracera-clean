# ==============================================================================
# api_client.py - Klien HTTP Terpusat untuk Komunikasi ke Backend
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
        except Exception as e:
            print(f"[APIClient Warning] fetch_filter_options fallback: {e}")
        return {
            "universities": [
                "Universitas Gadjah Mada", "Universitas Indonesia", "Institut Teknologi Bandung",
                "Institut Teknologi Sepuluh Nopember", "Universitas Airlangga", "BINUS University"
            ],
            "study_programs": [
                "All Study Programs",
                "Computer Science & Software Engineering",
                "Data Science & Quantitative Analytics",
                "Finance, Banking & Accounting",
                "Engineering & Industrial Technology",
                "Business, Management & Economics"
            ],
            "target_roles": [
                "Software Engineer", "Technical Lead", "Engineering Manager",
                "Data Analyst", "Data Scientist", "Data Lead",
                "Product Owner", "Product Manager", "Associate Product Manager",
                "DevOps Engineer", "Cloud Architect", "AI/ML Engineer"
            ],
            "industries": ["Technology", "Financial Services", "Consulting", "Consumer Goods", "Telecommunications"],
            "graduation_years": ["2027", "2026", "2025", "2024", "2023", "2022", "2021", "2020"],
            "starting_roles": ["Software Engineer", "Backend Developer", "Data Analyst", "Product Associate"],
            "career_levels": ["Entry-Level", "Mid-Senior", "Executive"]
        }

    @st.cache_data(ttl=300, show_spinner="Loading dashboard data...")
    def fetch_dashboard_data(
        _self,
        university=None,
        study_program=None,
        target_role=None,
        industry=None,
        graduation_year=None,
        starting_role=None,
        career_level=None,
        **kwargs
    ):
        """Mengambil metrik analitik lengkap dari backend."""
        params = {}
        if university and university != "All":
            params["university"] = university
        if study_program and study_program not in ["All", "All Study Programs"]:
            params["study_program"] = study_program
        if target_role and target_role != "All":
            params["target_role"] = target_role
        if industry and industry != "All":
            params["industry"] = industry
        if graduation_year and str(graduation_year) != "All":
            params["graduation_year"] = str(graduation_year)
        if starting_role and starting_role != "All":
            params["starting_role"] = starting_role
        if career_level and career_level != "All":
            params["career_level"] = career_level

        try:
            resp = requests.get(f"{_self.base_url}/analytics/dashboard", params=params, headers=_self.headers, timeout=10)
            if resp.status_code == 200:
                return resp.json(), True
            else:
                print(f"[APIClient Warning] Dashboard endpoint status {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"[APIClient Error] fetch_dashboard_data failed: {e}")
        return _self._generate_fallback_data(), False

    # Alias untuk kompatibilitas
    fetch_dashboard_analytics = fetch_dashboard_data

    @st.cache_data(ttl=300, show_spinner="Loading comparison data...")
    def fetch_skills_comparison(
        _self,
        universities_list,
        study_program=None,
        target_role=None,
        industry=None,
        graduation_year=None,
        starting_role=None,
        career_level=None,
        **kwargs
    ):
        """Mengambil data perbandingan multi-universitas dari endpoint backend."""
        unis_param = ",".join(universities_list)
        params = {"universities": unis_param}
        if study_program and study_program not in ["All", "All Study Programs"]:
            params["study_program"] = study_program
        if target_role and target_role != "All":
            params["target_role"] = target_role
        if industry and industry != "All":
            params["industry"] = industry
        if graduation_year and str(graduation_year) != "All":
            params["graduation_year"] = str(graduation_year)
        if starting_role and starting_role != "All":
            params["starting_role"] = starting_role
        if career_level and career_level != "All":
            params["career_level"] = career_level
            
        try:
            resp = requests.get(f"{_self.base_url}/analytics/skills/comparison", params=params, headers=_self.headers, timeout=10)
            if resp.status_code == 200:
                return resp.json(), True
            else:
                print(f"[APIClient Warning] Skills comparison endpoint returned status {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"[APIClient Error] fetch_skills_comparison failed: {e}")
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
                    {"rank": 6, "skill_name": "Docker & Containerization", "count": 76, "percentage": 31.7, "endorsements": 94, "demand_badge": "[Demand: ★★]", "bar_color": "#1d4ed8"},
                    {"rank": 7, "skill_name": "Git & Version Control", "count": 68, "percentage": 28.3, "endorsements": 82, "demand_badge": "[Demand: ★★]", "bar_color": "#1d4ed8"},
                    {"rank": 8, "skill_name": "CI/CD & DevOps Automation", "count": 58, "percentage": 24.2, "endorsements": 76, "demand_badge": "[Surging ▲]", "bar_color": "#f97316"},
                    {"rank": 9, "skill_name": "REST API & GraphQL Development", "count": 52, "percentage": 21.7, "endorsements": 64, "demand_badge": "[Demand: ★★]", "bar_color": "#1d4ed8"},
                    {"rank": 10, "skill_name": "Linux System Administration", "count": 46, "percentage": 19.2, "endorsements": 58, "demand_badge": "[Demand: ★★]", "bar_color": "#1d4ed8"}
                ],
                "soft_skills": [
                    {"rank": 1, "skill_name": "Problem Solving & Critical Thinking", "count": 210, "percentage": 87.5, "endorsements": 512, "demand_badge": "[Universal ★★★]", "bar_color": "#10b981"},
                    {"rank": 2, "skill_name": "Cross-functional Collaboration", "count": 178, "percentage": 74.2, "endorsements": 245, "demand_badge": "[High ★★]", "bar_color": "#10b981"},
                    {"rank": 3, "skill_name": "Stakeholder & Client Communication", "count": 134, "percentage": 55.8, "endorsements": 180, "demand_badge": "[Surging ▲]", "bar_color": "#f97316"},
                    {"rank": 4, "skill_name": "Agile & Scrum Coordination", "count": 126, "percentage": 52.5, "endorsements": 165, "demand_badge": "[Standard ★★]", "bar_color": "#10b981"},
                    {"rank": 5, "skill_name": "Adaptability & Continuous Learning", "count": 108, "percentage": 45.0, "endorsements": 140, "demand_badge": "[High ★★]", "bar_color": "#10b981"},
                    {"rank": 6, "skill_name": "Team Leadership & Mentoring", "count": 92, "percentage": 38.3, "endorsements": 125, "demand_badge": "[High ★★]", "bar_color": "#10b981"},
                    {"rank": 7, "skill_name": "Strategic Analytical Thinking", "count": 85, "percentage": 35.4, "endorsements": 110, "demand_badge": "[High ★★]", "bar_color": "#10b981"},
                    {"rank": 8, "skill_name": "Public Speaking & Presentation", "count": 78, "percentage": 32.5, "endorsements": 95, "demand_badge": "[High ★★]", "bar_color": "#10b981"},
                    {"rank": 9, "skill_name": "Time & Priority Management", "count": 70, "percentage": 29.2, "endorsements": 84, "demand_badge": "[Standard ★★]", "bar_color": "#10b981"},
                    {"rank": 10, "skill_name": "Conflict Resolution & Negotiation", "count": 62, "percentage": 25.8, "endorsements": 72, "demand_badge": "[Standard ★★]", "bar_color": "#10b981"}
                ]
            },
            "skills_distribution": {
                "categories": [
                    {"category": "Technical & Engineering", "percentage": 61.4, "total": 2850, "subcategories": {"Backend": 1368, "Cloud": 741, "Data": 513, "Other Tech": 228}},
                    {"category": "Soft Skills & Leadership", "percentage": 18.1, "total": 840, "subcategories": {"Communication": 420, "Problem Solving": 268, "Leadership": 152}},
                    {"category": "Business & Product Strategy", "percentage": 11.2, "total": 520, "subcategories": {"Project Mgmt": 302, "Product Owner": 145, "Business Analysis": 73}},
                    {"category": "Tools & Software Platforms", "percentage": 9.3, "total": 430, "subcategories": {"Dev Tools / IDEs": 224, "Software Platforms": 206}}
                ],
                "total_skills_count": 2850,
                "unique_skills_count": 2850
            },
            "skill_network": {
                "nodes": [
                    {"id": "python", "label": "Python", "category": "Hard Skill", "dimension": "Programming Language", "endorsements": 740, "frequency": 182, "pct": 75.8, "size": 38, "color": "#1d4ed8", "x": 0.0, "y": 0.0},
                    {"id": "sql", "label": "SQL", "category": "Hard Skill", "dimension": "Programming Language", "endorsements": 498, "frequency": 156, "pct": 65.0, "size": 32, "color": "#1d4ed8", "x": -0.35, "y": 0.25},
                    {"id": "cloud", "label": "Cloud Infra", "category": "Hard Skill", "dimension": "Technical Expertise", "endorsements": 315, "frequency": 112, "pct": 46.7, "size": 26, "color": "#0284c7", "x": 0.35, "y": 0.25},
                    {"id": "problem_solving", "label": "Problem Solving", "category": "Soft Skill", "dimension": "Problem Solving", "endorsements": 512, "frequency": 210, "pct": 87.5, "size": 34, "color": "#10b981", "x": 0.0, "y": -0.4},
                    {"id": "leadership", "label": "Leadership", "category": "Soft Skill", "dimension": "Leadership", "endorsements": 245, "frequency": 92, "pct": 38.3, "size": 24, "color": "#8b5cf6", "x": -0.45, "y": -0.2},
                    {"id": "communication", "label": "Communication", "category": "Soft Skill", "dimension": "Adaptability", "endorsements": 320, "frequency": 134, "pct": 55.8, "size": 28, "color": "#ec4899", "x": 0.45, "y": -0.2}
                ],
                "edges": [
                    {"source": "python", "target": "sql", "weight": 2.5},
                    {"source": "python", "target": "cloud", "weight": 2.0},
                    {"source": "python", "target": "problem_solving", "weight": 3.0},
                    {"source": "sql", "target": "problem_solving", "weight": 2.2},
                    {"source": "leadership", "target": "communication", "weight": 2.8},
                    {"source": "problem_solving", "target": "communication", "weight": 2.0}
                ],
                "central_hub": "Python"
            },
            "trending_gap": {
                "items": [
                    {"no": "01", "skill_name": "System Architecture", "skill_type": "Hard Skill", "alumni_count": 98, "alumni_pct": 40.8, "trend_30d_pct": 100.0, "market_demand_pct": 62.3, "gap_score": -21.5, "gap_status": "Critical Deficit", "target_roles": ["Software Engineer", "Technical Lead"]},
                    {"no": "02", "skill_name": "Cloud Infrastructure", "skill_type": "Tools & Infra", "alumni_count": 112, "alumni_pct": 46.7, "trend_30d_pct": 100.0, "market_demand_pct": 58.0, "gap_score": -11.3, "gap_status": "Emerging Shortage", "target_roles": ["DevOps Engineer", "Cloud Architect"]},
                    {"no": "03", "skill_name": "Problem Solving", "skill_type": "Soft Skill", "alumni_count": 210, "alumni_pct": 87.5, "trend_30d_pct": 38.0, "market_demand_pct": 90.0, "gap_score": -2.5, "gap_status": "Balanced Alignment", "target_roles": ["All Engineering Roles"]},
                    {"no": "04", "skill_name": "Python Programming", "skill_type": "Hard Skill", "alumni_count": 182, "alumni_pct": 75.8, "trend_30d_pct": 42.0, "market_demand_pct": 74.0, "gap_score": 1.8, "gap_status": "Competitive Advantage", "target_roles": ["Software Engineer", "Data Scientist"]},
                    {"no": "05", "skill_name": "SQL & Databases", "skill_type": "Hard Skill", "alumni_count": 156, "alumni_pct": 65.0, "trend_30d_pct": 35.0, "market_demand_pct": 68.0, "gap_score": -3.0, "gap_status": "Balanced Alignment", "target_roles": ["Data Analyst", "Backend Engineer"]}
                ],
                "total_job_postings_analyzed": 1200,
                "summary_insights": {
                    "hub": "Python serves as the primary connectivity hub (centrality 0.88), bridging Data Science, Backend API, and DevOps.",
                    "dominance": "Technical & Engineering represents 61.4% of total alumni skills, driven predominantly by Backend development.",
                    "gap": "System Architecture shows the largest deficit (-21.5%), with 62% hiring requirements vs 40.8% alumni ownership.",
                    "coverage": "Analysis extracted from 240 verified alumni profiles matched with active market benchmarks.",
                    "rank_combo": "Python + SQL + Problem Solving is held by 71.4% of alumni who advanced to Senior roles within 3 years.",
                    "rank_accel": "Cloud Infrastructure and API Design show +100% adoption velocity in recent alumni profiles over the last 30 days."
                }
            }
        }

    def _generate_fallback_comparison(self, universities_list):
        preset = {
            "Universitas Gadjah Mada": {
                "matched_alumni": 51, "ratio": "72% : 28%", "align_pct": 76.4, "label": "Leader", "vel": "CloudInfra (+35%)",
                "h_skills": [("Python Programming", 39, 76.5, "Safe", "safe"), ("SQL & Relational DB", 33, 64.7, "High Demand", "demand"), ("Cloud Infrastructure", 24, 47.1, "Emerging Gap", "gap"), ("System Architecture", 21, 41.2, "Critical Deficit", "deficit"), ("Data Structures", 19, 37.3, "High Demand", "demand")],
                "s_skills": [("Problem Solving", 44, 86.3), ("Cross-functional Collab.", 38, 74.5), ("Agile & Scrum Coord.", 27, 52.9), ("Stakeholder Comm.", 26, 51.0)],
                "sigs": [("Cloud Infrastructure & Microservices", "+14% vs benchmark"), ("Python Automation Pipelines", "+11% vs benchmark")]
            },
            "Universitas Indonesia": {
                "matched_alumni": 36, "ratio": "68% : 32%", "align_pct": 68.2, "label": "Moderate", "vel": "Python (+22%)",
                "h_skills": [("SQL & Relational DB", 26, 72.2, "Safe", "safe"), ("Python Programming", 23, 63.9, "High Demand", "demand"), ("Data Structures & Alg.", 17, 47.2, "High Demand", "demand"), ("Cloud Infrastructure", 14, 38.9, "Emerging Gap", "gap"), ("System Architecture", 11, 30.6, "Critical Deficit", "deficit")],
                "s_skills": [("Cross-functional Collab.", 29, 80.6), ("Problem Solving", 28, 77.8), ("Stakeholder Comm.", 21, 58.3), ("Agile & Scrum Coord.", 17, 47.2)],
                "sigs": [("Product Analytics & Strategy", "+16% vs benchmark"), ("SQL Database Optimization", "+9% vs benchmark")]
            },
            "Institut Teknologi Bandung": {
                "matched_alumni": 39, "ratio": "75% : 25%", "align_pct": 74.8, "label": "High", "vel": "Docker/K8s (+31%)",
                "h_skills": [("Python Programming", 27, 69.2, "Safe", "safe"), ("Docker & Containerization", 23, 59.0, "Safe", "safe"), ("System Architecture", 20, 51.3, "Emerging Gap", "gap"), ("Distributed Systems", 18, 46.2, "High Demand", "demand"), ("Cloud Infrastructure", 17, 43.6, "Emerging Gap", "gap")],
                "s_skills": [("Problem Solving", 31, 79.5), ("Technical Leadership", 25, 64.1), ("Cross-functional Collab.", 24, 61.5), ("Complex Systems Design", 19, 48.7)],
                "sigs": [("Kubernetes & Scalability Pipelines", "+19% vs benchmark"), ("Distributed Architecture", "+13% vs benchmark")]
            }
        }
        cards = []
        for u in universities_list:
            data = preset.get(u, {
                "matched_alumni": 25, "ratio": "70% : 30%", "align_pct": 70.0, "label": "High", "vel": "Python (+20%)",
                "h_skills": [("Python Programming", 18, 72.0, "Safe", "safe"), ("SQL & Databases", 15, 60.0, "High Demand", "demand"), ("Git & Version Control", 12, 48.0, "High Demand", "demand"), ("Cloud Fundamentals", 10, 40.0, "Emerging Gap", "gap"), ("API Development", 8, 32.0, "Critical Deficit", "deficit")],
                "s_skills": [("Problem Solving", 20, 80.0), ("Communication", 16, 64.0), ("Teamwork", 14, 56.0), ("Time Management", 10, 40.0)],
                "sigs": [(f"Core {u.split()[0]} Focus", "+10% vs benchmark")]
            })
            cards.append({
                "university_name": u,
                "micro_summary": {
                    "matched_alumni": data["matched_alumni"],
                    "skill_type_ratio": data["ratio"],
                    "market_alignment_pct": data["align_pct"],
                    "market_alignment_label": data["label"],
                    "highest_velocity_skill": data["vel"]
                },
                "top_hard_skills": [
                    {"rank": idx+1, "skill_name": item[0], "count": item[1], "percentage": item[2], "demand_badge": item[3], "badge_type": item[4]}
                    for idx, item in enumerate(data["h_skills"])
                ],
                "top_soft_skills": [
                    {"rank": idx+1, "skill_name": item[0], "count": item[1], "percentage": item[2], "demand_badge": "Soft Skill", "badge_type": "soft"}
                    for idx, item in enumerate(data["s_skills"])
                ],
                "signature_skills": [
                    {"skill_name": item[0], "diff_pct": item[1], "delta_vs_cohort": 10.0} for item in data["sigs"]
                ]
            })
        return {
            "selected_universities": universities_list,
            "comparison_cards": cards,
            "executive_takeaways": [
                {"title": "Strongest Technical Pipeline", "description": "Selected cohorts demonstrate solid foundations across data and software stacks.", "card_type": "default"},
                {"title": "Shared Critical Gap", "description": "System Architecture & Cloud Security average below 45% across selected universities.", "card_type": "critical"},
                {"title": "Highest Skill Diversity", "description": "Multi-campus benchmarking reveals complementary technical proficiencies.", "card_type": "default"},
                {"title": "Fastest Growing Skill", "description": "DevOps & cloud containerization show surging adoption velocity over 30 days.", "card_type": "success"}
            ]
        }

# ==============================================================================
# Instance Singleton untuk Ekspor
# ==============================================================================
api_client = APIClient()