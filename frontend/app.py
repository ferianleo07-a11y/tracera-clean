# ==============================================================================
# app.py - Integrated Streamlit Analytics Application (English UI Standard)
# Penanggung Jawab: Orang 4 (Frontend Lead)
# Lokasi: frontend/app.py
# Desain Bersih, Proporsional Sesuai Mockup Referensi Tracera
# ==============================================================================
import sys
from pathlib import Path

# 1. Resolusi Path: Menjamin modul dikenali baik dijalankan dari root maupun folder frontend
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
FRONTEND_DIR = Path(__file__).resolve().parent
if str(FRONTEND_DIR) not in sys.path:
    sys.path.insert(0, str(FRONTEND_DIR))

import streamlit as st

# Impor dengan fallback otomatis
try:
    from frontend.utils.api_client import api_client, APIClient
    from frontend.ui_components.headers import render_header
    from frontend.ui_components.filters import render_cohort_filters, render_kpi_metric_cards
    from frontend.ui_components.pilar1_skill_charts import (
        render_hard_vs_soft_skills, render_skills_distribution_by_category
    )
    from frontend.ui_components.pilar2_gap_charts import (
        render_skill_network_graph, render_trending_gap_table,
        render_insights_cards, render_skills_comparison
    )
except ModuleNotFoundError:
    from utils.api_client import api_client, APIClient
    from ui_components.headers import render_header
    from ui_components.filters import render_cohort_filters, render_kpi_metric_cards
    from ui_components.pilar1_skill_charts import (
        render_hard_vs_soft_skills, render_skills_distribution_by_category
    )
    from ui_components.pilar2_gap_charts import (
        render_skill_network_graph, render_trending_gap_table,
        render_insights_cards, render_skills_comparison
    )

# 2. Konfigurasi Halaman Dasar Clean Light Mode (Tanpa Sidebar)
st.set_page_config(
    page_title="Skills Intelligence - Tracera",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 3. Injeksi Kustom CSS Tema Clean Light Sesuai Standar Tracera & Gambar Mockup
st.markdown("""
<style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    section[data-testid="stSidebar"] {display: none !important;}
    div[data-testid="collapsedControl"] {display: none !important;}
    button[kind="headerNoPadding"] {display: none !important;}
    .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    
    /* Tombol Tertiary (Reset & Export CSV) - Polos Tanpa Kotak */
    button[kind="tertiary"] {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        color: #475569 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 4px 8px !important;
    }
    button[kind="tertiary"]:hover {
        color: #0f172a !important;
        background-color: #f1f5f9 !important;
    }

    /* Tombol Secondary (Share view) - Kotak Putih Membulat */
    button[kind="secondary"] {
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        border: 1px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
        padding: 5px 14px !important;
    }
    
    div[data-testid="stMetricValue"] {font-size: 24px; font-weight: 700; color: #0f172a;}
    .css-1544g2n {padding-top: 1rem;}

    /* Styling Segmented Control (Pills Tabs & View Toggle) */
    .stButtonGroup,
    div[data-testid="stButtonGroup"] {
        background-color: #f1f5f9 !important;
        padding: 3px !important;
        border-radius: 8px !important;
        width: fit-content !important;
        border: 1px solid #e2e8f0 !important;
    }
    .stButtonGroup button,
    div[data-testid="stButtonGroup"] button {
        border-radius: 6px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        padding: 4px 12px !important;
        color: #64748b !important;
        background-color: transparent !important;
    }
    /* Tab Aktif (Kartu Putih Bersih Tanpa Outline Biru) */
    .stButtonGroup button[aria-checked="true"],
    .stButtonGroup button[aria-pressed="true"],
    div[data-testid="stButtonGroup"] button[aria-checked="true"],
    div[data-testid="stButtonGroup"] button[aria-pressed="true"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-weight: 600 !important;
        border: none !important;
        outline: none !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
    }

    /* Mendorong View Toggle di kolom kanan 100% rata kanan sejajar tabel/kartu */
    div[data-testid="stColumn"]:has(div[data-testid="stButtonGroup"]) {
        display: flex !important;
        align-items: flex-end !important;
    }
    div[data-testid="stColumn"]:has(div[data-testid="stButtonGroup"]) div[data-testid="stElementContainer"] {
        display: flex !important;
        justify-content: flex-end !important;
        width: 100% !important;
    }
    div[data-testid="stColumn"] .stButtonGroup,
    div[data-testid="stColumn"] div[data-testid="stButtonGroup"] {
        margin-left: auto !important;
        align-self: flex-end !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # 4. Ambil data dropdown filter & payload dashboard terpusat dari FastAPI
    filter_opts = api_client.fetch_filter_options()
    uni = st.session_state.get("sel_uni", "All")
    prog = st.session_state.get("sel_prog", "All Study Programs")
    role = st.session_state.get("sel_role", "All")
    ind = st.session_state.get("sel_ind", "All")
    grad = st.session_state.get("sel_grad", "All")
    start_role = st.session_state.get("sel_start", "All")
    lvl = st.session_state.get("filter_lvl", "All")

    dashboard_data, is_conn = api_client.fetch_dashboard_data(
        university=uni,
        study_program=prog,
        target_role=role,
        industry=ind,
        graduation_year=grad,
        starting_role=start_role,
        career_level=lvl
    )

    # 5. Header Bar (Reset, Export CSV, Share view copy link)
    render_header(dashboard_data)

    # 6. Cohort Filters Bar & 4 Borderless KPI Cards
    render_cohort_filters(filter_opts)
    render_kpi_metric_cards(dashboard_data.get("kpi", {}))

    # 7. DUA TAB UTAMA DASHBOARD (Skills Explorer & Skills Comparison) Berupa Segmented Control (Rata Kiri)
    selected_tab = st.segmented_control(
        "Main Navigation",
        options=["Skills Explorer", "Skills Comparison"],
        default="Skills Explorer",
        label_visibility="collapsed",
        key="main_tab_select"
    ) or "Skills Explorer"

    st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)

    if selected_tab == "Skills Explorer":
        # Header Sub-View & Segmented Control Toggle: Ranking View vs Ecosystem View (Rata Kanan Penuh Sejajar Tabel)
        col_title, col_toggle = st.columns([7, 3], vertical_alignment="center")

        with col_toggle:
            subview = st.segmented_control(
                "Select View",
                options=["Ranking View", "Ecosystem View"],
                default="Ranking View",
                format_func=lambda x: f":material/leaderboard: {x}" if x == "Ranking View" else f":material/alt_route: {x}",
                label_visibility="collapsed",
                key="segmented_subview"
            ) or "Ranking View"

        with col_title:
            if subview == "Ranking View":
                st.markdown('''
                <div style="margin-bottom: 8px;">
                    <div style="font-size: 13.5px; font-weight: 700; color: #0f172a;">Top Skills Distribution: Hard Skills vs Soft Skills</div>
                    <div style="font-size: 11px; color: #64748b;">Comparative ranking of technical capabilities (Hard) vs interpersonal proficiencies (Soft) based on alumni frequency, endorsements, and market demand</div>
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
                render_skills_distribution_by_category(
                    dashboard_data.get("skills_distribution", {}),
                    unique_skills_count=dashboard_data.get("kpi", {}).get("total_unique_skills")
                )
            with c_net:
                render_skill_network_graph(dashboard_data.get("skill_network", {}))
            render_trending_gap_table(dashboard_data.get("trending_gap", {}))
            render_insights_cards(dashboard_data.get("trending_gap", {}), mode="ecosystem")
    else:
        render_skills_comparison(
            api_client,
            selected_university=uni,
            study_program=prog,
            target_role=role,
            industry=ind,
            graduation_year=grad,
            starting_role=start_role,
            career_level=lvl
        )

if __name__ == "__main__":
    main()