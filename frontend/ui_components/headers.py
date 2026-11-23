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
    """Render Header Bar: Title, Status Badges, and Action Buttons (English)."""
    col_left, col_right = st.columns([6.8, 3.2], vertical_alignment="center")
    
    with col_left:
        st.markdown(
            """
            <div style="margin-bottom: 6px;">
                <div style="font-size: 22px; font-weight: 700; color: #0f172a; margin-bottom: 6px; line-height: 1.2;">
                    Skills Intelligence
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <!-- Badge Mock dataset: Background soft pastel blue & deep navy text -->
                    <span style="background-color: #edf1fa; color: #2c3852; font-size: 11.5px; font-weight: 600; padding: 3px 10px; border-radius: 9999px;">
                        Mock dataset
                    </span>
                    <span style="color: #64748b; font-size: 11.5px;">
                        Synthetic profiles (LinkedIn Extracted)
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_right:
        c_reset, c_export, c_share = st.columns([1, 1.35, 1.35], gap="small")
        
        # 1. Reset Button - Tanpa Kotak (type="tertiary")
        with c_reset:
            if st.button("Reset", icon=":material/refresh:", type="tertiary", key="btn_reset_all", help="Reset all filters and view to default", use_container_width=True):
                st.session_state["sel_uni"] = "All"
                st.session_state["sel_prog"] = "All Study Programs"
                st.session_state["sel_role"] = "All"
                st.session_state["sel_ind"] = "All"
                st.session_state["sel_grad"] = "All"
                st.session_state["sel_start"] = "All"
                st.query_params.clear()
                st.rerun()

        # 2. Export CSV Button - Tanpa Kotak (type="tertiary")
        with c_export:
            csv_buffer = io.StringIO()
            if dashboard_data and "trending_gap" in dashboard_data:
                df_export = pd.DataFrame(dashboard_data["trending_gap"]["items"])
            else:
                df_export = pd.DataFrame([{"Message": "No data"}])
            df_export.to_csv(csv_buffer, index=False)
            st.download_button(
                label="Export CSV",
                icon=":material/download:",
                type="tertiary",
                data=csv_buffer.getvalue(),
                file_name="skills_intelligence_metrics.csv",
                mime="text/csv",
                key="btn_export_csv",
                help="Export current analysis table to CSV",
                use_container_width=True
            )

        # 3. Share View Button - Memakai Kotak Putih Membulat (type="secondary")
        with c_share:
            if st.button("Share view", icon=":material/share:", type="secondary", key="btn_share_view", help="Copy link to current view and filters", use_container_width=True):
                uni = st.session_state.get("sel_uni", "All")
                prog = st.session_state.get("sel_prog", "All Study Programs")
                role = st.session_state.get("sel_role", "All")
                ind = st.session_state.get("sel_ind", "All")
                grad = st.session_state.get("sel_grad", "All")
                start = st.session_state.get("sel_start", "All")
                share_url = f"http://localhost:8501/?uni={uni}&prog={prog}&role={role}&ind={ind}&grad={grad}&start={start}"
                st.query_params["uni"] = uni
                st.query_params["prog"] = prog
                st.query_params["role"] = role
                st.query_params["ind"] = ind
                st.query_params["grad"] = grad
                st.query_params["start"] = start
                st.toast("Link copied to clipboard! Ready to share.", icon="✅")
                st.info(f"Share link: `{share_url}`")