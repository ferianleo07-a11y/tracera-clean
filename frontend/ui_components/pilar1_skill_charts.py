import plotly.graph_objects as go
import streamlit as st

def render_hard_vs_soft_skills(hard_soft_data):
    """Render Ranking View: Dual Column Progress Bar Hard vs Soft Skills (English)."""
    hard_items = hard_soft_data.get("hard_skills", [])
    soft_items = hard_soft_data.get("soft_skills", [])
    c_hard, c_soft = st.columns(2)
    with c_hard:
        st.markdown('''
        &lt;div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 14px;"&gt;
            &lt;div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;"&gt;
                &lt;div style="font-size: 13px; font-weight: 700; color: #0f172a;"&gt;Top Hard Skills &amp; Tools&lt;/div&gt;
                &lt;span style="background: #eff6ff; color: #1d4ed8; font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 4px;"&gt;Top 6 Rank&lt;/span&gt;
            &lt;/div&gt;
            &lt;div style="font-size: 11px; color: #64748b; margin-bottom: 12px;"&gt;72% of skill ecosystem (Average 8.1 per profile)&lt;/div&gt;
        ''', unsafe_allow_html=True)
        for item in hard_items[:6]:
            rank, name = item["rank"], item["skill_name"]
            cnt, pct, end = item["count"], item["percentage"], item["endorsements"]
            badge, color = item["demand_badge"], item["bar_color"]
            badge_color = "#dc2626" if "Deficit" in badge else ("#d97706" if "Surging" in badge else "#1d4ed8")
            st.markdown(f'''
            &lt;div style="margin-bottom: 8px;"&gt;
                &lt;div style="display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 600; margin-bottom: 2px;"&gt;
                    &lt;span style="color: #0f172a;"&gt;{rank}. {name}&lt;/span&gt;
                    &lt;span style="font-size: 10.5px; color: #475569;"&gt;{cnt} alumni ({pct}%) &middot; {end} endorsements &lt;span style="color: {badge_color};"&gt;{badge}&lt;/span&gt;&lt;/span&gt;
                &lt;/div&gt;
                &lt;div style="background: #f1f5f9; height: 6px; border-radius: 3px; overflow: hidden;"&gt;
                    &lt;div style="background: {color}; width: {pct}%; height: 100%; border-radius: 3px;"&gt;&lt;/div&gt;
                &lt;/div&gt;
            &lt;/div&gt;
            ''', unsafe_allow_html=True)
        st.markdown('''
            &lt;div style="text-align: right; margin-top: 8px;"&gt;
                &lt;span style="color: #1d4ed8; font-size: 11px; font-weight: 600; cursor: pointer;"&gt;View Top 10 Hard Skills &rarr;&lt;/span&gt;
            &lt;/div&gt;
        &lt;/div&gt;
        ''', unsafe_allow_html=True)
    with c_soft:
        st.markdown('''
        &lt;div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 14px;"&gt;
            &lt;div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;"&gt;
                &lt;div style="font-size: 13px; font-weight: 700; color: #0f172a;"&gt;Top Soft Skills &amp; Leadership&lt;/div&gt;
                &lt;span style="background: #fdf2f8; color: #be185d; font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 4px;"&gt;Top 6 Rank&lt;/span&gt;
            &lt;/div&gt;
            &lt;div style="font-size: 11px; color: #64748b; margin-bottom: 12px;"&gt;28% of skill ecosystem (Average 3.2 per profile)&lt;/div&gt;
        ''', unsafe_allow_html=True)
        for item in soft_items[:6]:
            rank, name = item["rank"], item["skill_name"]
            cnt, pct, end = item["count"], item["percentage"], item["endorsements"]
            badge, color = item["demand_badge"], item["bar_color"]
            badge_color = "#16a34a" if "Universal" in badge or "High" in badge else ("#d97706" if "Surging" in badge else "#64748b")
            st.markdown(f'''
            &lt;div style="margin-bottom: 8px;"&gt;
                &lt;div style="display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 600; margin-bottom: 2px;"&gt;
                    &lt;span style="color: #0f172a;"&gt;{rank}. {name}&lt;/span&gt;
                    &lt;span style="font-size: 10.5px; color: #475569;"&gt;{cnt} alumni ({pct}%) &middot; {end} endorsements &lt;span style="color: {badge_color};"&gt;{badge}&lt;/span&gt;&lt;/span&gt;
                &lt;/div&gt;
                &lt;div style="background: #f1f5f9; height: 6px; border-radius: 3px; overflow: hidden;"&gt;
                    &lt;div style="background: {color}; width: {pct}%; height: 100%; border-radius: 3px;"&gt;&lt;/div&gt;
                &lt;/div&gt;
            &lt;/div&gt;
            ''', unsafe_allow_html=True)
        st.markdown('''
            &lt;div style="text-align: right; margin-top: 8px;"&gt;
                &lt;span style="color: #be185d; font-size: 11px; font-weight: 600; cursor: pointer;"&gt;View Top 10 Soft Skills &rarr;&lt;/span&gt;
            &lt;/div&gt;
        &lt;/div&gt;
        ''', unsafe_allow_html=True)

def render_skills_distribution_by_category(skills_dist_data):
    """Render Ecosystem View Sisi Kiri (Horizontal Stacked Bar) - English UI."""
    st.markdown('''
    &lt;div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 14px;"&gt;
        &lt;div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;"&gt;
            &lt;div style="font-size: 13px; font-weight: 700; color: #0f172a;"&gt;Skills Distribution by Category&lt;/div&gt;
            &lt;span style="background: #f1f5f9; color: #475569; font-size: 10.5px; font-weight: 600; padding: 2px 6px; border-radius: 4px;"&gt;2,850 Total Skills&lt;/span&gt;
        &lt;/div&gt;
        &lt;div style="font-size: 11px; color: #64748b; margin-bottom: 10px;"&gt;Segmented by industry taxonomy and technical depth&lt;/div&gt;
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
            hovertemplate="&lt;b&gt;%{y}&lt;/b&gt;&lt;br&gt;" + subcat + ": %{x:,} entries&lt;extra&gt;&lt;/extra&gt;"
        ))
    fig.update_layout(
        barcdmode='stack', height=260, showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="#ffffff", paper_bgcolor="#ffffff"
    )
    fig.update_xaxes(showgrid=True, gridcolor="#f1f5f9", tickfont=dict(size=8.5, color="#64748b"))
    fig.update_yaxes(tickfont=dict(size=9, color="#1e293b", weight="bold"))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('''
        &lt;div style="display: flex; justify-content: space-between; font-size: 11px; color: #64748b; margin-top: 4px;"&gt;
            &lt;span&gt;Showing accumulated skill entries across profiles&lt;/span&gt;
            &lt;span style="color: #1d4ed8; cursor: pointer; font-weight: 600;"&gt;Open full taxonomy &rarr;&lt;/span&gt;
        &lt;/div&gt;
    &lt;/div&gt;
    ''', unsafe_allow_html=True)