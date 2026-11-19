# ==============================================================================
# headers.py - Komponen Header Bar, Actions dan Clipboard Share Link (English UI)
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
            <div style="margin-bottom: 6px;">
                <div style="font-size: 11px; color: #64748b; font-weight: 500; margin-bottom: 3px;">
                    ferian's Workspace &nbsp;&rsaquo;&nbsp; Career Intelligence &nbsp;&rsaquo;&nbsp; <span style="color: #0f172a; font-weight: 600;">Skills Intelligence</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 18px; font-weight: 700; color: #0f172a;">
                        Skills Intelligence
                    </span>
                    <span style="background-color: #ede9fe; color: #6d28d9; font-size: 10.5px; font-weight: 600; padding: 2px 7px; border-radius: 4px;">
                        Mock dataset
                    </span>
                    <span style="color: #64748b; font-size: 11px;">
                        Synthetic profiles (LinkedIn Extracted)
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_right:
        c_reset, c_export, c_share = st.columns([1, 1.3, 1.2])
        # 1. Reset Button
        with c_reset:
            if st.button("Reset", key="btn_reset_all", help="Reset all filters and view to default"):
                st.session_state["sel_uni"] = "All"
                st.session_state["sel_prog"] = "All Study Programs"
                st.session_state["sel_role"] = "All"
                st.session_state["sel_ind"] = "All"
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
                uni = st.session_state.get("sel_uni", "All")
                prog = st.session_state.get("sel_prog", "All Study Programs")
                role = st.session_state.get("sel_role", "All")
                ind = st.session_state.get("sel_ind", "All")
                share_url = f"http://localhost:8501/?uni={uni}&prog={prog}&role={role}&ind={ind}"
                st.query_params["uni"] = uni
                st.query_params["prog"] = prog
                st.query_params["role"] = role
                st.query_params["ind"] = ind
                st.toast("Link copied to clipboard! Ready to share.", icon="✅")
                st.info(f"Share link: `{share_url}`")
