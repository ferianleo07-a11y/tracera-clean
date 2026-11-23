# ==============================================================================
# filters.py - Cohort Filters Bar dan 4 Borderless KPI Metric Cards (English UI)
# Penanggung Jawab: Orang 4 (Frontend Lead)
# Lokasi: frontend/ui_components/filters.py
# ==============================================================================
import streamlit as st

def render_cohort_filters(filter_options):
    """Render Cohort Filters Bar: Dropdowns (English)."""
    if "sel_uni" not in st.session_state:
        st.session_state["sel_uni"] = st.query_params.get("uni", "All")
    if "sel_prog" not in st.session_state:
        st.session_state["sel_prog"] = st.query_params.get("prog", "All Study Programs")
    if "sel_role" not in st.session_state:
        st.session_state["sel_role"] = st.query_params.get("role", "All")
    if "sel_ind" not in st.session_state:
        st.session_state["sel_ind"] = st.query_params.get("ind", "All")
    if "sel_grad" not in st.session_state:
        st.session_state["sel_grad"] = st.query_params.get("grad", "All")
    if "sel_start" not in st.session_state:
        st.session_state["sel_start"] = st.query_params.get("start", "All")

    st.markdown(
        """
        <div style="font-size: 13px; font-weight: 600; color: #0f172a; margin-top: 4px; margin-bottom: 6px;">
            Cohort filters
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)
    unis = ["All"] + [u for u in filter_options.get("universities", []) if u != "All"]
    progs = ["All Study Programs"] + [p for p in filter_options.get("study_programs", []) if p not in ["All", "All Study Programs"]]
    roles = ["All"] + [r for r in filter_options.get("target_roles", []) if r != "All"]
    idx_uni = unis.index(st.session_state["sel_uni"]) if st.session_state["sel_uni"] in unis else 0
    idx_prog = progs.index(st.session_state["sel_prog"]) if st.session_state["sel_prog"] in progs else 0
    idx_role = roles.index(st.session_state["sel_role"]) if st.session_state["sel_role"] in roles else 0
    with c1:
        st.selectbox("University", unis, index=idx_uni, key="sel_uni")
    with c2:
        st.selectbox("Study program", progs, index=idx_prog, key="sel_prog")
    with c3:
        st.selectbox("Target role", roles, index=idx_role, key="sel_role")
    with st.expander("+ More filters", expanded=True):
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            grads = ["All"] + [str(g) for g in filter_options.get("graduation_years", []) if str(g) != "All"]
            idx_grad = grads.index(str(st.session_state["sel_grad"])) if str(st.session_state["sel_grad"]) in grads else 0
            st.selectbox("Graduation year", grads, index=idx_grad, key="sel_grad")
        with m2:
            starts = ["All"] + [s for s in filter_options.get("starting_roles", []) if s != "All"]
            idx_start = starts.index(st.session_state["sel_start"]) if st.session_state["sel_start"] in starts else 0
            st.selectbox("Starting role", starts, index=idx_start, key="sel_start")
        with m3:
            inds = ["All"] + [i for i in filter_options.get("industries", ["Technology", "Financial Services", "Consulting", "Consumer Goods", "Telecommunications"]) if i != "All"]
            idx_ind = inds.index(st.session_state["sel_ind"]) if st.session_state["sel_ind"] in inds else 0
            st.selectbox("Industry", inds, index=idx_ind, key="sel_ind")
        with m4:
            st.selectbox("Career level", ["All", "Entry-Level", "Mid-Senior", "Executive"], key="filter_lvl")
    st.markdown("<hr style='border: none; border-top: 1px solid #f1f5f9; margin: 10px 0 14px 0;'/>", unsafe_allow_html=True)
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
                <div style="padding: 2px 8px;">
                    <div style="font-size: 11.5px; font-weight: 500; color: #64748b; margin-bottom: 2px;">
                        {label}
                    </div>
                    <div style="display: flex; align-items: baseline; gap: 6px;">
                        <span style="font-size: 24px; font-weight: 700; color: #0f172a; letter-spacing: -0.3px;">
                            {val}
                        </span>
                        <span style="font-size: 11.5px; font-weight: 600; color: {mom_color};">
                            {sub}
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    st.markdown("<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 12px 0 16px 0;'/>", unsafe_allow_html=True)