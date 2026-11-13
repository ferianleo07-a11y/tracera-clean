# ==============================================================================
# headers.py - Komponen Header Bar, Actions & Clipboard Share Link (English UI)
# Penanggung Jawab: Orang 4 (Frontend Lead)
# Lokasi: frontend/ui_components/headers.py
# Desain Bersih, Proporsional & Minimalis Sesuai Mockup Tracera
# ==============================================================================
import io
import pandas as pd
import streamlit as st

def render_header(dashboard_data=None):
    """Render Header Bar: Breadcrumb, Title, Status Badges, and Action Buttons (English)."""
    col_left, col_right = st.columns([6, 4], vertical_alignment="center")
    
    with col_left:
        st.markdown(
            """
            &lt;div style="margin-bottom: 6px;"&gt;
                &lt;div style="font-size: 11px; color: #64748b; font-weight: 500; margin-bottom: 3px;"&gt;
                    ferian's Workspace &amp;nbsp;&amp;rsaquo;&amp;nbsp; Career Intelligence &amp;nbsp;&amp;rsaquo;&amp;nbsp; &lt;span style="color: #0f172a; font-weight: 600;"&gt;Skills Intelligence&lt;/span&gt;
                &lt;/div&gt;
                &lt;div style="display: flex; align-items: center; gap: 8px;"&gt;
                    &lt;span style="font-size: 18px; font-weight: 700; color: #0f172a;"&gt;
                        Skills Intelligence
                    &lt;/span&gt;
                    &lt;span style="background-color: #ede9fe; color: #6d28d9; font-size: 10.5px; font-weight: 600; padding: 2px 7px; border-radius: 4px;"&gt;
                        Mock dataset
                    &lt;/span&gt;
                    &lt;span style="color: #64748b; font-size: 11px;"&gt;
                        Synthetic profiles (LinkedIn Extracted)
                    &lt;/span&gt;
                &lt;/div&gt;
            &lt;/div&gt;
            """,
            unsafe_allow_html=True
        )

with col_right:
    c_reset, c_export, c_share = st.columns([1, 1.3, 1.2])
    # 1. Reset Button
    with c_reset:
        if st.button("Reset", key="btn_reset_all", help="Reset all filters and view to default"):
            st.session_state["filter_uni"] = "Universitas Gadjah Mada"
            st.session_state["filter_prog"] = "All Study Programs"
            st.session_state["filter_role"] = "Software Engineer / Tech Roles"
            st.session_state["filter_ind"] = "Technology"
            st.query_params.clear()
            st.rerun()
    # 2. Export CSV Button
    with c_export:
        csv_buffer = io.StringIO()
        if dashboard_data and "trending_gap" in dashboard_data:
            df_export = pd.DataFrame(dashboard_data["trending_gap"]["items"])
        else:
            df_export = pd.DataFrame([{"Message": "No data"}])
        df_export.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Export CSV",
            data=csv_buffer.getvalue(),
            file_name="skills_intelligence_metrics.csv",
            mime="text/csv",
            key="btn_export_csv",
            help="Export current analysis table to CSV"
        )
    # 3. Share View Button
    with c_share:
        if st.button("Share view", key="btn_share_view", help="Copy link to current view and filters"):
            uni = st.session_state.get("filter_uni", "Universitas Gadjah Mada")
            prog = st.session_state.get("filter_prog", "All Study Programs")
            role = st.session_state.get("filter_role", "Software Engineer / Tech Roles")
            ind = st.session_state.get("filter_ind", "Technology")
            share_url = f"http://localhost:8501/?uni={uni}&prog={prog}&role={role}&ind={ind}"
            st.query_params["uni"] = uni
            st.query_params["prog"] = prog
            st.query_params["role"] = role
            st.query_params["ind"] = ind
            st.toast("Link copied to clipboard! Ready to share.", icon="✅")
            st.info(f"Share link: `{share_url}`")