# ==============================================================================
# filters.py - Cohort Filters Bar & 4 Borderless KPI Metric Cards (English UI)
# Penanggung Jawab: Orang 4 (Frontend Lead)
# Lokasi: frontend/ui_components/filters.py
# ==============================================================================
import streamlit as st

def render_cohort_filters(filter_options):
    """Render Cohort Filters Bar: Dropdowns and Reset Filters (English)."""
    if "filter_uni" not in st.session_state:
        st.session_state["filter_uni"] = st.query_params.get("uni", "Universitas Gadjah Mada")
    if "filter_prog" not in st.session_state:
        st.session_state["filter_prog"] = st.query_params.get("prog", "All Study Programs")
    if "filter_role" not in st.session_state:
        st.session_state["filter_role"] = st.query_params.get("role", "Software Engineer / Tech Roles")
    if "filter_ind" not in st.session_state:
        st.session_state["filter_ind"] = st.query_params.get("ind", "Technology")
    c_filt_head, c_reset_filt = st.columns([8, 2], vertical_alignment="center")
    with c_filt_head:
        st.markdown(
            """
            &lt;div style="font-size: 13px; font-weight: 600; color: #0f172a; margin-top: 4px; margin-bottom: 4px;"&gt;
                Cohort filters
            &lt;/div&gt;
            """,
            unsafe_allow_html=True
        )
    with c_reset_filt:
        if st.button("Reset filters", key="btn_reset_filters_only", help="Reset cohort filters to All"):
            st.session_state["filter_uni"] = "All"
            st.session_state["filter_prog"] = "All"
            st.session_state["filter_role"] = "All"
            st.session_state["filter_ind"] = "All"
            st.query_params.clear()
            st.rerun()

    c1, c2, c3 = st.columns(3)
    unis = ["All"] + [u for u in filter_options.get("universities", []) if u != "All"]
    progs = ["All Study Programs"] + [p for p in filter_options.get("study_programs", []) if p not in ["All", "All Study Programs"]]
    roles = ["Software Engineer / Tech Roles", "All"] + [r for r in filter_options.get("target_roles", []) if r not in ["All", "Software Engineer / Tech Roles"]]
    idx_uni = unis.index(st.session_state["filter_uni"]) if st.session_state["filter_uni"] in unis else 0
    idx_prog = progs.index(st.session_state["filter_prog"]) if st.session_state["filter_prog"] in progs else 0
    idx_role = roles.index(st.session_state["filter_role"]) if st.session_state["filter_role"] in roles else 0
    with c1:
        st.session_state["filter_uni"] = st.selectbox("University", unis, index=idx_uni, key="sel_uni")
    with c2:
        st.session_state["filter_prog"] = st.selectbox("Study program", progs, index=idx_prog, key="sel_prog")
    with c3:
        st.session_state["filter_role"] = st.selectbox("Target role", roles, index=idx_role, key="sel_role")
    with st.expander("+ More filters", expanded=True):
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.selectbox("Graduation year", ["All", "2024", "2023", "2022", "2021"], key="filter_grad")
        with m2:
            st.selectbox("Starting role", ["All", "Junior Developer", "Intern", "Analyst"], key="filter_start")
        with m3:
            inds = ["Technology", "All", "Financial Services", "Consulting",   "Consumer Goods", "Telecommunications"]
            idx_ind = inds.index(st.session_state["filter_ind"]) if st.session_state["filter_ind"] in inds else 0
            st.session_state["filter_ind"] = st.selectbox("Industry", inds, index=idx_ind, key="sel_ind")
        with m4:
            st.selectbox("Career level", ["Mid-Senior", "Entry-Level", "Executive", "All"], key="filter_lvl")
        with m5:
            st.selectbox("Location", ["Indonesia", "Singapore", "Remote", "All"], key="filter_loc")
    st.markdown("&lt;hr style='border: none; border-top: 1px solid #f1f5f9; margin: 10px 0 14px 0;'/&gt;", unsafe_allow_html=True)
def render_kpi_metric_cards(kpi_data):
    """Render 4 Borderless KPI Metric Cards (English)."""
    k1, k2, k3, k4 = st.columns(4)
    metrics = [
        ("Matched alumni", f"{kpi_data.get('matched_alumni', 240):,}", "alumni"),
        ("Total unique skills", f"{kpi_data.get('total_unique_skills', 2850):,}", "skills"),
        ("Skill type ratio (H : S)", f"{kpi_data.get('skill_type_ratio', '72% : 28%')}", "Hard vs Soft"),
        ("Trending skills", f"{kpi_data.get('trending_skills_count', 55)}", kpi_data.get('mom_growth_str', "+18% MoM"))
    ]
    
    for col, (label, val, sub) in zip([k1, k2, k3, k4], metrics):
        with col:
            mom_color = "#16a34a" if "+" in sub else "#64748b"
            st.markdown(
                f"""
                &lt;div style="padding: 2px 8px;"&gt;
                    &lt;div style="font-size: 11.5px; font-weight: 500; color: #64748b; margin-bottom: 2px;"&gt;
                        {label}
                    &lt;/div&gt;
                    &lt;div style="display: flex; align-items: baseline; gap: 6px;"&gt;
                        &lt;span style="font-size: 24px; font-weight: 700; color: #0f172a; letter-spacing: -0.3px;"&gt;
                            {val}
                        &lt;/span&gt;
                        &lt;span style="font-size: 11.5px; font-weight: 600; color: {mom_color};"&gt;
                            {sub}
                        &lt;/span&gt;
                    &lt;/div&gt;
                &lt;/div&gt;
                """,
                unsafe_allow_html=True
            )
    st.markdown("&lt;hr style='border: none; border-top: 1px solid #e2e8f0; margin: 12px 0 16px 0;'/&gt;", unsafe_allow_html=True)