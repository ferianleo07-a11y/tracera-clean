import plotly.graph_objects as go
import streamlit as st

def render_skill_network_graph(network_data):
    """Render Ecosystem View Sisi Kanan (Co-occurrence Network Graph) - English UI."""
    st.markdown('''
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
            <div style="font-size: 13px; font-weight: 700; color: #0f172a;">Skill Co-occurrence Network Graph</div>
            <span style="background: #e0f2fe; color: #0284c7; font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 4px;">Dense Cluster</span>
        </div>
        <div style="font-size: 11px; color: #64748b; margin-bottom: 8px;">Correlation of skills frequently co-appearing on alumni profiles</div>
    ''', unsafe_allow_html=True)
    nodes = network_data.get("nodes", [])
    edges = network_data.get("edges", [])
    edge_x, edge_y = [], []
    node_map = {n["id"]: n for n in nodes}
    for e in edges:
        s, t = node_map.get(e["source"]), node_map.get(e["target"])
        if s and t:
            edge_x.extend([s.get("x", 0), t.get("x", 0), None])
            edge_y.extend([s.get("y", 0), t.get("y", 0), None])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=1.6, color='#cbd5e1'), hoverinfo='none'))
    node_x = [n.get("x", 0) for n in nodes]
    node_y = [n.get("y", 0) for n in nodes]
    node_size = [n.get("size", 20) for n in nodes]
    node_color = [n.get("color", "#0284c7") for n in nodes]
    node_text = [n.get("label", "") for n in nodes]
    hover_text = [f"<b>{n['label']}</b><br>Dimension: {n['dimension']}<br>Endorsements: {n['endorsements']}<br>Alumni: {n['frequency']} ({n['pct']}%)" for n in nodes]
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y, mode='markers+text',
        marker=dict(size=node_size, color=node_color, line=dict(width=1.8, color='#ffffff')),
        text=node_text, textposition='middle center',
        textfont=dict(size=8.5, color='#ffffff', family='Arial Black'),
        hoverinfo='text', hovertext=hover_text
    ))
    fig.update_layout(
        height=260, showlegend=False, margin=dict(l=5, r=5, t=5, b=5),
        plot_bgcolor='#f8fafc', paper_bgcolor='#ffffff',
        xaxis=dict(visible=False), yaxis=dict(visible=False)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('''
        <div style="font-size: 10px; color: #64748b; margin-top: 4px; text-align: center;">
            Node size = endorsement volume &middot; Line = co-occurrence strength &middot; <span style="color: #1d4ed8; cursor: pointer;">Filter node: &blacktriangledown;</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def render_trending_gap_table(gap_data):
    """Render Tabel 'Trending Skills & Market Gap Analysis' (English UI)."""
    st.markdown('''
    <div style="margin-top: 18px; margin-bottom: 6px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="font-size: 14px; font-weight: 700; color: #0f172a;">Trending Skills &amp; Market Gap Analysis</div>
            <span style="font-size: 11px; color: #64748b;">Calculated from 1,200+ Active Job Postings</span>
        </div>
        <div style="font-size: 11px; color: #64748b; margin-top: 2px;">
            Skill acceleration analysis (30-day velocity) compared against industry hiring demand benchmarks
        </div>
    </div>
    ''', unsafe_allow_html=True)
    items = gap_data.get("items", [])
    header_html = '''
    <table style="width: 100%; border-collapse: collapse; font-size: 11.5px; margin-bottom: 12px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden;">
        <tr style="border-bottom: 1px solid #e2e8f0; background: #f8fafc; color: #475569; text-align: left; font-size: 10.5px; text-transform: uppercase;">
            <th style="padding: 7px 9px;">No</th><th>Skill Name</th><th>Skill Type</th>
            <th>Alumni Frequency</th><th>30d Trend</th><th>Market Gap Analysis (Supply vs Demand)</th>
            <th>Target Career Roles</th><th style="text-align: right; padding-right: 10px;">Action</th>
        </tr>'''
    rows_html = ""
    for it in items:
        badge_type = "#dbeafe; color: #1e40af;" if "Hard" in it["skill_type"] else ("#fce7f3; color: #be185d;" if "Soft" in it["skill_type"] else "#f3e8ff; color: #7e22ce;")
        gap_color = "#dc2626" if "Critical" in it["gap_status"] or "Shortage" in it["gap_status"] else ("#d97706" if "Moderate" in it["gap_status"] else "#16a34a")
        gap_bg = "#fef2f2" if "Critical" in it["gap_status"] or "Shortage" in it["gap_status"] else ("#fffbeb" if "Moderate" in it["gap_status"] else "#f0fdf4")
        roles_str = ", ".join(it["target_roles"])
        rows_html += f'''
        <tr style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 7px 9px; font-weight: 600; color: #94a3b8;">{it["no"]}</td>
            <td style="font-weight: 600; color: #0f172a;">{it["skill_name"]}</td>
            <td><span style="background: {badge_type} padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: 600;">{it["skill_type"]}</span></td>
             <td style="color: #334155;">{it["alumni_count"]} alumni ({it["alumni_pct"]}%)</td>
            <td style="color: #16a34a; font-weight: 600;">&blacktriangle; +{it["trend_30d_pct"]}%</td>
            <td><span style="background: {gap_bg}; color: {gap_color}; padding: 2px 6px; border-radius: 4px; font-weight: 600; font-size: 10.5px;">{it["gap_score"]:+.1f}% ({it["gap_status"]})</span></td>
            <td style="color: #475569; font-size: 11px;">{roles_str}</td>
            <td style="text-align: right; padding-right: 10px;"><span style="color: #1d4ed8; font-weight: 600; cursor: pointer; border: 1px solid #bfdbfe; padding: 2px 6px; border-radius: 4px; font-size: 10px;">Explore &rarr;</span></td>
        </tr>'''
    st.markdown(header_html + rows_html + "</table>", unsafe_allow_html=True)

def render_insights_cards(gap_data, mode="ranking"):
    """Render 4 Kartu Wawasan Eksekutif (English UI)."""
    insights = gap_data.get("summary_insights", {})
    c1, c2, c3, c4 = st.columns(4)
    if mode == "ranking":
        cards = [
            ("Dominant Skill Combination", insights.get("rank_combo", "Python + SQL + Problem Solving is held by 71.4% of alumni reaching Senior level within 3 years.")),
            ("Highest Hard Skill Velocity", insights.get("rank_accel", "Cloud Infrastructure and API Design recorded +100% velocity in recent alumni profiles.")),
            ("Critical Market Gap", insights.get("gap", "System Architecture exhibits the largest deficit (-21.5%) vs hiring demand.")),
            ("Profile Data Coverage", insights.get("coverage", "Analysis extracted from 240 verified alumni profiles matched with market datasets."))
        ]
    else:
        cards = [
            ("Central Connectivity Hub", insights.get("hub", "Python acts as the central connectivity hub (0.88 centrality), bridging Data Science and DevOps.")),
            ("Technical Category Dominance", insights.get("dominance", "Technical & Engineering represents 61.4% of total alumni skills, dominated by Backend.")),
            ("Critical Market Gap", insights.get("gap", "System Architecture exhibits the largest deficit (-21.5%) vs hiring demand.")),
            ("Profile Data Coverage", insights.get("coverage", "Analysis extracted from 240 verified alumni profiles matched with market datasets."))
        ]
    for col, (title, desc) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(f'''
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px; height: 100%;">
                <div style="font-size: 11px; font-weight: 700; color: #0f172a; margin-bottom: 3px;">{title}</div>
                <div style="font-size: 10px; color: #475569; line-height: 1.35;">{desc}</div>
            </div>
            ''', unsafe_allow_html=True)

def render_skills_comparison(comparison_data):
    """
    Render Tab 2: Skills Comparison View (Side-by-Side 3 Kolom Berdampingan).
    Fitur Lengkap: Sub-Header 6 Checkbox Universitas, Kotak Merah Metrik Mikro,
    Top Hard Skills dengan Integrasi Benchmark Pasar, Top Soft Skills,
    Signature Skills (+ vs Cohort), dan 4 Kartu Executive Takeaways.
    """

    st.markdown('''
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px;">
        <div style="font-size: 13.5px; font-weight: 700; color: #0f172a; margin-bottom: 2px;">Compare observed skills &amp; benchmark alignment</div>
        <div style="font-size: 11px; color: #64748b; margin-bottom: 8px;">Select 2–3 universities. Cohort filters apply.</div>
    </div>
    ''', unsafe_allow_html=True)

    cb_cols = st.columns(6)
    all_unis = [
        "Universitas Gadjah Mada", "Universitas Indonesia", "Institut Teknologi Bandung",
        "Institut Teknologi Sepuluh Nopember", "Universitas Airlangga", "BINUS University"
    ]
    selected_unis = []
    defaults = ["Universitas Gadjah Mada", "Universitas Indonesia", "Institut Teknologi Bandung"]
    for idx, (col, u_name) in enumerate(zip(cb_cols, all_unis)):
        with col:
            chk = st.checkbox(u_name, value=(u_name in defaults), key=f"cb_univ_{idx}")
            if chk:
                selected_unis.append(u_name)
    if len(selected_unis) < 2:
        st.warning("Please select at least 2 universities to compare.")
        selected_unis = defaults[:2]
    cards_data = comparison_data.get("comparison_cards", [])
    active_cards = [c for c in cards_data if c["university_name"] in selected_unis][:3]

    cols = st.columns(len(active_cards))
    for col, card in zip(cols, active_cards):
        u_name = card["university_name"]
        m = card["micro_summary"]
        h_skills = card.get("top_hard_skills", [])
        s_skills = card.get("top_soft_skills", [])
        sigs = card.get("signature_skills", [])
        with col:

            st.markdown(f'''
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; display: flex; flex-direction: column;">
                <div style="font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #f1f5f9;">
                    {u_name}
                </div>
            ''', unsafe_allow_html=True)

            align_badge = f'<span style="background: #dcfce7; color: #15803d; font-size: 10px; font-weight: 700; padding: 1px 5px; border-radius: 4px; margin-left: 4px;">{m["market_alignment_label"]}</span>' if m["market_alignment_label"] in ["Leader", "High"] else f'<span style="background: #f1f5f9; color: #475569; font-size: 10px; font-weight: 700; padding: 1px 5px; border-radius: 4px; margin-left: 4px;">{m["market_alignment_label"]}</span>'
            st.markdown(f'''
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 12px; margin-bottom: 14px; display: flex; flex-direction: column; gap: 6px; font-size: 11.5px;">
                <div style="display: flex; justify-content: space-between;"><span style="color: #64748b;">Matched alumni</span><span style="font-weight: 600;">{m["matched_alumni"]}</span></div>
                <div style="display: flex; justify-content: space-between;"><span style="color: #64748b;">Skill type ratio (H:S)</span><span style="font-weight: 600;">{m["skill_type_ratio"]}</span></div>
                <div style="display: flex; justify-content: space-between; align-items: center;"><span style="color: #64748b;">Market Alignment</span><span style="font-weight: 600;">{m["market_alignment_pct"]}% {align_badge}</span></div>
                <div style="display: flex; justify-content: space-between;"><span style="color: #64748b;">Highest Skill Velocity</span><span style="font-weight: 600; colo
                r: #0f172a;">{m["highest_velocity_skill"]}</span></div>
            </div>
            ''', unsafe_allow_html=True)

            st.markdown('<div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.3px; color: #475569; margin-bottom: 8px;">Top Hard Skills &middot; Market Benchmark</div>', unsafe_allow_html=True)
            for h in h_skills[:5]:
                bg_badge = "#dcfce7; color: #166534;" if h["badge_type"] == "safe" else ("#fee2e2; color: #991b1b;" if h["badge_type"] == "deficit" else ("#fef3c7; color: #92400e;" if h["badge_type"] == "gap" else "#f1f5f9; color: #475569;"))
                st.markdown(f'''
                <div style="margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; font-size: 11.5px; margin-bottom: 2px;">
                        <span style="color: #1e293b; font-weight: 500;">{h["rank"]}. {h["skill_name"]}</span>
                        <span style="font-size: 10.5px; color: #64748b;">{h["count"]} ({h["percentage"]}%) <span style="background: {bg_badge} font-size: 9.5px; padding: 1px 5px; border-radius: 3px; font-weight: 600;">{h["demand_badge"]}</span></span>
                    </div>
                    <div style="width: 100%; height: 4px; background: #e2e8f0; border-radius: 2px;">
                        <div style="width: {h['percentage']}%; height: 100%; background: #2563eb; border-radius: 2px;"></div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

            st.markdown('<div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.3px; color: #475569; margin-top: 12px; margin-bottom: 8px;">Top Soft Skills</div>', unsafe_allow_html=True)
            for s in s_skills[:4]:
                st.markdown(f'''
                <div style="margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; font-size: 11.5px; margin-bottom: 2px;">
                        <span style="color: #1e293b; font-weight: 500;">{s["rank"]}. {s["skill_name"]}</span>
                        <span style="font-size: 10.5px; color: #64748b;">{s["count"]} ({s["percentage"]}%)</span>
                    </div>
                    <div style="width: 100%; height: 4px; background: #e2e8f0; border-radius: 2px;">
                        <div style="width: {s['percentage']}%; height: 100%; background: #7c3aed; border-radius: 2px;"></div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

            st.markdown('<div style="border-top: 1px dashed #e2e8f0; padding-top: 10px; margin-top: 10px;"><div style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: #475569; margin-bottom: 6px;">Signature Skills (vs Cohort)</div>', unsafe_allow_html=True)
            for sig in sigs[:2]:
                st.markdown(f'''
                <div style="display: flex; justify-content: space-between; font-size: 11.5px; margin-bottom: 4px;">
                    <span style="color: #1e293b; font-weight: 500;">{sig["skill_name"]}</span>
                    <span style="color: #16a34a; font-weight: 600; font-size: 11px;">{sig["diff_pct"]}</span>
                </div>
                ''', unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="margin-top: 18px;"></div>', unsafe_allow_html=True)
    t_cols = st.columns(4)
    takeaways = comparison_data.get("executive_takeaways", [])
    for col, t in zip(t_cols, takeaways):
        card_bg = "#fff5f5; border-color: #fecaca;" if t["card_type"] == "critical" else ("#f0fdf4; border-color: #bbf7d0;" if t["card_type"] == "success" else "#ffffff; border-color: #e2e8f0;")
        title_color = "#991b1b" if t["card_type"] == "critical" else ("#166534" if t["card_type"] == "success" else "#0f172a")
        desc_color = "#7f1d1d" if t["card_type"] == "critical" else ("#14532d" if t["card_type"] == "success" else "#64748b")
        with col:
            st.markdown(f'''
            <div style="background: {card_bg} border: 1px solid; border-radius: 8px; padding: 12px 14px; height: 100%;">
                <div style="font-size: 11.5px; font-weight: 700; color: {title_color}; margin-bottom: 4px;">{t["title"]}</div>
                <div style="font-size: 11px; color: {desc_color}; line-height: 1.4;">{t["description"]}</div>
            </div>
            ''', unsafe_allow_html=True)
def render_skill_details(dashboard_data):
    """Komponen Tab 3: Skill Details (Preview Antarmuka Frontend - English UI)."""
    selected_skill = st.selectbox("Select Skill for In-depth Analysis:", [
        "Python Programming", "System Architecture & Microservices",
        "Cloud Infrastructure (AWS/GCP)", "Problem Solving & Critical Thinking"
    ])
    st.markdown(f'''
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 14px; margin-top: 6px;">
        <div style="font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 2px;">{selected_skill}</div>
        <div style="font-size: 11.5px; color: #64748b;">Category: Technical &amp; Engineering &middot; Relevance Score: 94%</div>
        <hr style="border: none; border-top: 1px solid #f1f5f9; margin: 10px 0;"/>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; font-size: 11.5px;">
            <div>
                <b>Total Endorsements:</b><br/>
                <span style="font-size: 20px; font-weight: 700; color: #1d4ed8;">740</span> peer validations
            </div>
            <div>
                <b>Primary Career Targets:</b><br/>
                1. Software Engineer (65%)<br/>2. Data Scientist (25%)<br/>3. Cloud Architect (10%)
            </div>
            <div>
                <b>Top Hiring Organizations:</b><br/>
                &bull; Shopee, GoTo, BCA, Telkom Indonesia, Tiket.com
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    st.success(f"Career Preparedness: Alumni with {selected_skill} achieve an average hiring absorption of 2.1 months post-graduation.")
