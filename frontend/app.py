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
    render_insights_cards, render_skills_comparison
)
# 1. Konfigurasi Halaman Dasar Clean Light Mode (Tanpa Sidebar)
st.set_page_config(
    page_title="Skills Intelligence - Tracera",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# 2. Injeksi Kustom CSS Tema Clean Light Sesuai Standar Tracera
st.markdown("""
<style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    section[data-testid="stSidebar"] {display: none !important;}
    div[data-testid="collapsedControl"] {display: none !important;}
    button[kind="headerNoPadding"] {display: none !important;}
    .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    button[kind="secondary"] {border-radius: 4px; font-size: 11.5px; font-weight: 500;}
    div[data-testid="stMetricValue"] {font-size: 24px; font-weight: 700; color: #0f172a;}
    .css-1544g2n {padding-top: 1rem;}
</style>
""", unsafe_allow_html=True)

def main():
    # 3. Ambil data dropdown filter & payload dashboard terpusat dari FastAPI
    filter_opts = api_client.fetch_filter_options()
    uni = st.session_state.get("sel_uni", "All")
    prog = st.session_state.get("sel_prog", "All Study Programs")
    role = st.session_state.get("sel_role", "All")
    ind = st.session_state.get("sel_ind", "All")
    grad = st.session_state.get("sel_grad", "All")
    start_role = st.session_state.get("sel_start", "All")

    dashboard_data, is_conn = api_client.fetch_dashboard_data(uni, prog, role, ind, grad, start_role)

    # 5. Header Bar (Reset, Export CSV, Share view copy link)
    render_header(dashboard_data)

    # 6. Cohort Filters Bar &amp; 4 Borderless KPI Cards
    render_cohort_filters(filter_opts)
    render_kpi_metric_cards(dashboard_data.get("kpi", {}))

    # 6. DUA TAB UTAMA DASHBOARD (Skills Explorer & Skills Comparison)
    tab_explorer, tab_comparison = st.tabs([
        "Skills Explorer", "Skills Comparison"
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
        render_skills_comparison(
            api_client,
            study_program=prog,
            target_role=role,
            industry=ind,
            graduation_year=grad,
            starting_role=start_role
        )
if __name__ == "__main__":
    main()
