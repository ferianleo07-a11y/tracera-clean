# ==============================================================================
# app.py - Integrated Streamlit Analytics Application (English UI Standard)
# Penanggung Jawab: Orang 4 (Frontend Lead)
# Lokasi: frontend/app.py
# Desain Bersih, Proporsional Sesuai Mockup Referensi Tracera
# ==============================================================================
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
&lt;style&gt;
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    button[kind="secondary"] {border-radius: 4px; font-size: 11.5px; font-weight: 500;}
    div[data-testid="stMetricValue"] {font-size: 24px; font-weight: 700; color: #0f172a;}
    .css-1544g2n {padding-top: 1rem;}
&lt;/style&gt;
""", unsafe_allow_html=True)
# 3. Sidebar Navigasi Tracera Bersih Berbahasa Inggris (Tanpa Emoticon)
with st.sidebar:
    st.markdown('''
    &lt;div style="font-size: 17px; font-weight: 800; color: #0f172a; margin-bottom: 16px;"&gt;
        Tracera
    &lt;/div&gt;
    &lt;div style="font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px;"&gt;WORK&lt;/div&gt;
    &lt;div style="font-size: 12px; color: #475569; padding: 3px 0;"&gt;Search&lt;/div&gt;
    &lt;div style="font-size: 12px; color: #475569; padding: 3px 0;"&gt;Bulk Upload&lt;/div&gt;
    &lt;div style="font-size: 12px; color: #475569; padding: 3px 0;"&gt;Enrichment&lt;/div&gt;
    &lt;div style="font-size: 12px; color: #94a3b8; padding: 3px 0;"&gt;Enrichment Studio [Locked]&lt;/div&gt;
    &lt;br/&gt;
    &lt;div style="font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px;"&gt;DATA&lt;/div&gt;
    &lt;div style="font-size: 12px; color: #475569; padding: 3px 0;"&gt;Data sources&lt;/div&gt;
    &lt;div style="font-size: 12px; color: #475569; padding: 3px 0;"&gt;Active services&lt;/div&gt;
    &lt;div style="font-size: 12px; color: #475569; padding: 3px 0;"&gt;Snapshots&lt;/div&gt;
    &lt;br/&gt;
    &lt;div style="font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px;"&gt;CAREER INTELLIGENCE&lt;/div&gt;
    &lt;div style="font-size: 12px; color: #94a3b8; padding: 3px 0;"&gt;Analytics [Locked]&lt;/div&gt;
    &lt;div style="font-size: 12px; color: #475569; padding: 3px 0;"&gt;Alumni Repository&lt;/div&gt;
    &lt;div style="font-size: 12px; color: #475569; padding: 3px 0;"&gt;Career Paths&lt;/div&gt;
    &lt;div style="font-size: 12px; color: #94a3b8; padding: 3px 0;"&gt;Industry Insights [Locked]&lt;/div&gt;
    &lt;div style="font-size: 12px; color: #475569; padding: 3px 0;"&gt;Employer Network&lt;/div&gt;
    &lt;div style="font-size: 12px; color: #1d4ed8; font-weight: 700; background: #eff6ff; padding: 4px 8px; border-radius: 4px; margin: 2px 0;"&gt;
        Skills Intelligence
    &lt;/div&gt;
    &lt;div style="font-size: 12px; color: #94a3b8; padding: 3px 0;"&gt;Career Benchmark [Locked]&lt;/div&gt;
    ''', unsafe_allow_html=True)

def main():
    # 4. Ambil data dropdown filter &amp; payload dashboard terpusat dari FastAPI
    filter_opts = api_client.fetch_filter_options()
    uni = st.session_state.get("filter_uni", "Universitas Gadjah Mada")
    prog = st.session_state.get("filter_prog", "All Study Programs")
    role = st.session_state.get("filter_role", "Software Engineer / Tech Roles")
    ind = st.session_state.get("filter_ind", "Technology")

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
                &lt;div style="margin-bottom: 8px;"&gt;
                &lt;div style="font-size: 13.5px; font-weight: 700; color: #0f172a;"&gt;Top Skills Distribution: Hard Skills vs Soft Skills&lt;/div&gt;
                &lt;div style="font-size: 11px; color: #64748b;"&gt;Comparative ranking of technical capabilities (Hard) vs interpersonal proficiencies (Soft) based on alumni frequency, e
                ndorsements, and market demand&lt;/div&gt;
                &lt;/div&gt;
                ''', unsafe_allow_html=True)
            else:
                st.markdown('''
                &lt;div style="margin-bottom: 8px;"&gt;
                &lt;div style="font-size: 13.5px; font-weight: 700; color: #0f172a;"&gt;Skills Ecosystem &amp; Network (Ecosystem View)&lt;/div&gt;
                &lt;div style="font-size: 11px; color: #64748b;"&gt;Holistic map of alumni skill taxonomy based on industry categories and co-occurrence correlation graph&lt;/div&gt;
                &lt;/div&gt;
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
