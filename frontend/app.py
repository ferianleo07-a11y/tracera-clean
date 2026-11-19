# ==============================================================================
# app.py - Integrated Streamlit Analytics Application (English UI Standard)
# Penanggung Jawab: Orang 4 (Frontend Lead)
# Lokasi: frontend/app.py
# Desain Bersih, Proporsional Sesuai Mockup Referensi Tracera
# ==============================================================================
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from frontend.utils.api_client import api_client
from frontend.ui_components.headers import render_header
from frontend.ui_components.filters import render_cohort_filters, render_kpi_metric_cards
from frontend.ui_components.pilar1_skill_charts import (
    render_hard_vs_soft_skills, render_skills_distribution_by_category
)
from frontend.ui_components.pilar2_gap_charts import (
    render_skill_network_graph, render_trending_gap_table,
    render_insights_cards, render_skills_comparison, render_skill_details
)
# 1. Konfigurasi Halaman Dasar Clean Light Mode
st.set_page_config(
    page_title="Skills Intelligence - Tracera",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)
# 2. Injeksi Kustom CSS Tema Clean Light Sesuai Standar Tracera
st.markdown("""
<style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    button[kind="secondary"] {border-radius: 4px; font-size: 11.5px; font-weight: 500;}
    div[data-testid="stMetricValue"] {font-size: 24px; font-weight: 700; color: #0f172a;}
    .css-1544g2n {padding-top: 1rem;}
</style>
""", unsafe_allow_html=True)
# 3. Sidebar Navigasi Tracera Bersih Berbahasa Inggris (Tanpa Emoticon)
with st.sidebar:
    st.markdown('''
    <div style="font-size: 17px; font-weight: 800; color: #0f172a; margin-bottom: 16px;">
        Tracera
    </div>
    <div style="font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px;">WORK</div>
    <div style="font-size: 12px; color: #475569; padding: 3px 0;">Search</div>
    <div style="font-size: 12px; color: #475569; padding: 3px 0;">Bulk Upload</div>
    <div style="font-size: 12px; color: #475569; padding: 3px 0;">Enrichment</div>
    <div style="font-size: 12px; color: #94a3b8; padding: 3px 0;">Enrichment Studio [Locked]</div>
    <br/>
    <div style="font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px;">DATA</div>
    <div style="font-size: 12px; color: #475569; padding: 3px 0;">Data sources</div>
    <div style="font-size: 12px; color: #475569; padding: 3px 0;">Active services</div>
    <div style="font-size: 12px; color: #475569; padding: 3px 0;">Snapshots</div>
    <br/>
    <div style="font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px;">CAREER INTELLIGENCE</div>
    <div style="font-size: 12px; color: #94a3b8; padding: 3px 0;">Analytics [Locked]</div>
    <div style="font-size: 12px; color: #475569; padding: 3px 0;">Alumni Repository</div>
    <div style="font-size: 12px; color: #475569; padding: 3px 0;">Career Paths</div>
    <div style="font-size: 12px; color: #94a3b8; padding: 3px 0;">Industry Insights [Locked]</div>
    <div style="font-size: 12px; color: #475569; padding: 3px 0;">Employer Network</div>
    <div style="font-size: 12px; color: #1d4ed8; font-weight: 700; background: #eff6ff; padding: 4px 8px; border-radius: 4px; margin: 2px 0;">
        Skills Intelligence
    </div>
    <div style="font-size: 12px; color: #94a3b8; padding: 3px 0;">Career Benchmark [Locked]</div>
    ''', unsafe_allow_html=True)

def main():
    # 4. Ambil data dropdown filter & payload dashboard terpusat dari FastAPI
    filter_opts = api_client.fetch_filter_options()
    uni = st.session_state.get("filter_uni", "All")
    prog = st.session_state.get("filter_prog", "All Study Programs")
    role = st.session_state.get("filter_role", "All")
    ind = st.session_state.get("filter_ind", "All")

    dashboard_data, is_conn = api_client.fetch_dashboard_data(uni, prog, role, ind)

    # 5. Header Bar (Reset, Export CSV, Share view copy link)
    render_header(dashboard_data)

    # 6. Cohort Filters Bar &amp; 4 Borderless KPI Cards
    render_cohort_filters(filter_opts)
    render_kpi_metric_cards(dashboard_data.get("kpi", {}))

    # 7. TIGA TAB UTAMA DASHBOARD
    tab_explorer, tab_comparison, tab_details = st.tabs([
        "Skills Explorer", "Skills Comparison", "Skill Details"
    ])
    with tab_explorer:
        # Header Sub-View &amp; Radio Toggle: Ranking View vs Ecosystem View
        col_title, col_toggle = st.columns([7, 3], vertical_alignment="center")
        with col_toggle:
            subview = st.radio(
                "Select View",
                ["Ranking View", "Ecosystem View"],
                horizontal=True,
                label_visibility="collapsed",
                key="radio_subview"
            )

        with col_title:
            if subview == "Ranking View":
                st.markdown('''
                <div style="margin-bottom: 8px;">
                <div style="font-size: 13.5px; font-weight: 700; color: #0f172a;">Top Skills Distribution: Hard Skills vs Soft Skills</div>
                <div style="font-size: 11px; color: #64748b;">Comparative ranking of technical capabilities (Hard) vs interpersonal proficiencies (Soft) based on alumni frequency, e
                ndorsements, and market demand</div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown('''
                <div style="margin-bottom: 8px;">
                <div style="font-size: 13.5px; font-weight: 700; color: #0f172a;">Skills Ecosystem &amp; Network (Ecosystem View)</div>
                <div style="font-size: 11px; color: #64748b;">Holistic map of alumni skill taxonomy based on industry categories and co-occurrence correlation graph</div>
                </div>
                ''', unsafe_allow_html=True)
        # Konten Sesuai Mode Toggle Terpilih
        if subview == "Ranking View":
            render_hard_vs_soft_skills(dashboard_data.get("hard_soft_skills", {}))
            render_trending_gap_table(dashboard_data.get("trending_gap", {}))
            render_insights_cards(dashboard_data.get("trending_gap", {}), mode="ranking")
        else:
            c_dist, c_net = st.columns([1.1, 0.9])
            with c_dist:
                render_skills_distribution_by_category(dashboard_data.get("skills_distribution", {}))
            with c_net:
                render_skill_network_graph(dashboard_data.get("skill_network", {}))
            render_trending_gap_table(dashboard_data.get("trending_gap", {}))
            render_insights_cards(dashboard_data.get("trending_gap", {}), mode="ecosystem")
    with tab_comparison:
        # Ambil data komparasi multi-kampus dari backend
        target_default_unis = ["Universitas Gadjah Mada", "Universitas Indonesia", "Institut Teknologi Bandung"]
        comparison_data, is_comp_conn = api_client.fetch_skills_comparison(
        target_default_unis, study_program=prog, target_role=role, industry=ind
        )
        render_skills_comparison(comparison_data)

    with tab_details:
        render_skill_details(dashboard_data)
if __name__ == "__main__":
    main()
