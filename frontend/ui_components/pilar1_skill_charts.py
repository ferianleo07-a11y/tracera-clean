import plotly.graph_objects as go
import streamlit as st

def render_hard_vs_soft_skills(hard_soft_data):
    """Render Ranking View: Dual Column Progress Bar Hard vs Soft Skills (English)."""
    hard_items = hard_soft_data.get("hard_skills", [])
    soft_items = hard_soft_data.get("soft_skills", [])
    c_hard, c_soft = st.columns(2)
    with c_hard:
        st.markdown('''
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
                <div style="font-size: 13px; font-weight: 700; color: #0f172a;">Top Hard Skills &amp; Tools</div>
                <span style="background: #eff6ff; color: #1d4ed8; font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 4px;">Top 6 Rank</span>
            </div>
            <div style="font-size: 11px; color: #64748b; margin-bottom: 12px;">72% of skill ecosystem (Average 8.1 per profile)</div>
        ''', unsafe_allow_html=True)
        hard_palette = ["#2563eb", "#0ea5e9", "#f97316", "#14b8a6", "#6366f1", "#ef4444"]
        for idx, item in enumerate(hard_items[:6]):
            rank, name = item["rank"], item["skill_name"]
            cnt, pct, end = item["count"], item["percentage"], item["endorsements"]
            badge = item["demand_badge"]
            color = hard_palette[idx % len(hard_palette)]
            badge_color = "#dc2626" if "Deficit" in badge else ("#d97706" if "Surging" in badge else "#1d4ed8")
            st.markdown(f'''
            <div style="margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 600; margin-bottom: 2px;">
                    <span style="color: #0f172a;">{rank}. {name}</span>
                    <span style="font-size: 10.5px; color: #475569;">{cnt} alumni ({pct}%) &middot; {end} endorsements <span style="color: {badge_color};">{badge}</span></span>
                </div>
                <div style="background: #f1f5f9; height: 6px; border-radius: 3px; overflow: hidden;">
                    <div style="background: {color}; width: {pct}%; height: 100%; border-radius: 3px;"></div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c_soft:
        st.markdown('''
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
                <div style="font-size: 13px; font-weight: 700; color: #0f172a;">Top Soft Skills &amp; Leadership</div>
                <span style="background: #fdf2f8; color: #be185d; font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 4px;">Top 6 Rank</span>
            </div>
            <div style="font-size: 11px; color: #64748b; margin-bottom: 12px;">28% of skill ecosystem (Average 3.2 per profile)</div>
        ''', unsafe_allow_html=True)
        soft_palette = ["#10b981", "#7c3aed", "#ec4899", "#f59e0b", "#06b6d4", "#8b5cf6"]
        for idx, item in enumerate(soft_items[:6]):
            rank, name = item["rank"], item["skill_name"]
            cnt, pct, end = item["count"], item["percentage"], item["endorsements"]
            badge = item["demand_badge"]
            color = soft_palette[idx % len(soft_palette)]
            badge_color = "#16a34a" if "Universal" in badge or "High" in badge else ("#d97706" if "Surging" in badge else "#64748b")
            st.markdown(f'''
            <div style="margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 600; margin-bottom: 2px;">
                    <span style="color: #0f172a;">{rank}. {name}</span>
                    <span style="font-size: 10.5px; color: #475569;">{cnt} alumni ({pct}%) &middot; {end} endorsements <span style="color: {badge_color};">{badge}</span></span>
                </div>
                <div style="background: #f1f5f9; height: 6px; border-radius: 3px; overflow: hidden;">
                    <div style="background: {color}; width: {pct}%; height: 100%; border-radius: 3px;"></div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def render_skills_distribution_by_category(skills_dist_data):
    """Render Ecosystem View Sisi Kiri (Horizontal Stacked Bar) - English UI."""
    st.markdown('''
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
            <div style="font-size: 13px; font-weight: 700; color: #0f172a;">Skills Distribution by Category</div>
            <span style="background: #f1f5f9; color: #475569; font-size: 10.5px; font-weight: 600; padding: 2px 6px; border-radius: 4px;">2,850 Total Skills</span>
        </div>
        <div style="font-size: 11px; color: #64748b; margin-bottom: 10px;">Segmented by industry taxonomy and technical depth</div>
    ''', unsafe_allow_html=True)
    cats = skills_dist_data.get("categories", [])
    categories_order = ["Tools & Software Platforms", "Business & Product Strategy", "Soft Skills & Leadership", "Technical & Engineering"]
    subcat_colors = {
        "Backend": "#1d4ed8", "Cloud": "#38bdf8", "Data": "#60a5fa", "Other Tech": "#93c5fd",
        "Communication": "#0d9488", "Problem Solving": "#14b8a6", "Leadership": "#2dd4bf",
        "Project Mgmt": "#d97706", "Product Owner": "#f59e0b", "Business Analysis": "#fbbf24",
        "Git / Docker": "#7c3aed", "Jira / Agile": "#a855f7", "CI/CD Tools": "#c084fc"
    }
    fig = go.Figure()
    all_subcats = set()
    for c in cats:
        all_subcats.update(c.get("subcategories", {}).keys())
    for subcat in sorted(list(all_subcats)):
        x_vals, y_vals, text_vals = [], [], []
        for cat_name in categories_order:
            row = next((c for c in cats if c["category"] == cat_name), None)
            if row and subcat in row.get("subcategories", {}):
                cnt = row["subcategories"][subcat]
                x_vals.append(cnt)
                y_vals.append(cat_name)
                text_vals.append(f"{subcat} ({cnt:,})")
            else:
                x_vals.append(0)
                y_vals.append(cat_name)
                text_vals.append("")
        fig.add_trace(go.Bar(
            y=y_vals, x=x_vals, name=subcat, orientation='h',
            marker_color=subcat_colors.get(subcat, "#94a3b8"),
            text=text_vals, textposition='inside', insidetextanchor='middle',
            hovertemplate="<b>%{y}</b><br>" + subcat + ": %{x:,} entries<extra></extra>"
        ))
    fig.update_layout(
        barmode='stack', height=260, showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="#ffffff", paper_bgcolor="#ffffff"
    )
    fig.update_xaxes(showgrid=True, gridcolor="#f1f5f9", tickfont=dict(size=8.5, color="#64748b"))
    fig.update_yaxes(tickfont=dict(size=9, color="#1e293b", weight="bold"))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('''
        <div style="display: flex; justify-content: space-between; font-size: 11px; color: #64748b; margin-top: 4px;">
            <span>Showing accumulated skill entries across profiles</span>
            <span style="color: #1d4ed8; cursor: pointer; font-weight: 600;">Open full taxonomy &rarr;</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)