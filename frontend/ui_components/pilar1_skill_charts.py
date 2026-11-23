import plotly.graph_objects as go
import streamlit as st

def render_hard_vs_soft_skills(hard_soft_data):
    """Render Ranking View: Dual Column Progress Bar Hard vs Soft Skills (English)."""
    # 1. State limit independen untuk Hard Skills dan Soft Skills
    if "top_hard_skills_limit" not in st.session_state:
        st.session_state["top_hard_skills_limit"] = 6
    if "top_soft_skills_limit" not in st.session_state:
        st.session_state["top_soft_skills_limit"] = 6

    hard_limit = st.session_state["top_hard_skills_limit"]
    soft_limit = st.session_state["top_soft_skills_limit"]

    badge_hard = f"Top {hard_limit} Rank"
    badge_soft = f"Top {soft_limit} Rank"

    # Label dengan huruf 't' kecil sesuai permintaan ("Show top 10")
    lbl_hard = "Show top 10" if hard_limit == 6 else "Show top 6"
    lbl_soft = "Show top 10" if soft_limit == 6 else "Show top 6"

    # Ikon panah chevron resmi Google Material Symbols
    icon_hard = ":material/keyboard_arrow_down:" if hard_limit == 6 else ":material/keyboard_arrow_up:"
    icon_soft = ":material/keyboard_arrow_down:" if soft_limit == 6 else ":material/keyboard_arrow_up:"

    # 2. CSS agar tombol pill kompak, teks dan panah berada tepat di tengah
    st.markdown("""
    <style>
    /* Wrapper tombol agar tepat berada di tengah bawah kartu */
    div.st-key-btn_toggle_hard_skills,
    div.st-key-btn_toggle_soft_skills {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin-top: 10px !important;
        margin-bottom: 2px !important;
    }

    /* Tombol berbentuk kapsul kompak (tidak melar lebar) */
    div.st-key-btn_toggle_hard_skills button,
    div.st-key-btn_toggle_soft_skills button {
        border-radius: 9999px !important;
        font-size: 11px !important;
        font-weight: 500 !important;
        padding: 3px 14px !important;
        border: 1px solid #e2e8f0 !important;
        background-color: #ffffff !important;
        color: #1e293b !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
        height: 28px !important;
        min-height: 28px !important;
        max-height: 28px !important;
        width: auto !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 4px !important;
        cursor: pointer !important;
        transition: all 0.15s ease-in-out !important;
    }

    /* Hover halus */
    div.st-key-btn_toggle_hard_skills button:hover,
    div.st-key-btn_toggle_soft_skills button:hover {
        border-color: #cbd5e1 !important;
        color: #0f172a !important;
        background-color: #f8fafc !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06) !important;
    }

    /* Teks 'Show top 10' terkunci persis di tengah */
    div.st-key-btn_toggle_hard_skills button div[data-testid="stMarkdownContainer"],
    div.st-key-btn_toggle_soft_skills button div[data-testid="stMarkdownContainer"] {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div.st-key-btn_toggle_hard_skills button p,
    div.st-key-btn_toggle_soft_skills button p {
        margin: 0 !important;
        padding: 0 !important;
        font-size: 11px !important;
        font-weight: 500 !important;
        color: #1e293b !important;
        line-height: 1 !important;
    }

    /* Ukuran ikon panah chevron yang presisi */
    div.st-key-btn_toggle_hard_skills button [data-testid="stIconMaterial"],
    div.st-key-btn_toggle_soft_skills button [data-testid="stIconMaterial"] {
        font-size: 16px !important;
        width: 16px !important;
        height: 16px !important;
        line-height: 16px !important;
        color: #475569 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

    hard_items = hard_soft_data.get("hard_skills", [])
    soft_items = hard_soft_data.get("soft_skills", [])
    c_hard, c_soft = st.columns(2)

    # ==================== KOLOM HARD SKILLS ====================
    with c_hard:
        st.markdown(f'''
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
                <div style="font-size: 13px; font-weight: 700; color: #0f172a;">Top Hard Skills &amp; Tools</div>
                <span style="background: #eff6ff; color: #1d4ed8; font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 4px;">{badge_hard}</span>
            </div>
            <div style="font-size: 11px; color: #64748b; margin-bottom: 12px;">72% of skill ecosystem (Average 8.1 per profile)</div>
        ''', unsafe_allow_html=True)
        hard_palette = ["#2563eb", "#0ea5e9", "#f97316", "#14b8a6", "#6366f1", "#ef4444", "#8b5cf6", "#06b6d4", "#f59e0b", "#ec4899"]
        for idx, item in enumerate(hard_items[:hard_limit]):
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

        if st.button(lbl_hard, key="btn_toggle_hard_skills", icon=icon_hard, icon_position="right"):
            st.session_state["top_hard_skills_limit"] = 10 if hard_limit == 6 else 6
            st.rerun()

    # ==================== KOLOM SOFT SKILLS ====================
    with c_soft:
        st.markdown(f'''
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
                <div style="font-size: 13px; font-weight: 700; color: #0f172a;">Top Soft Skills &amp; Leadership</div>
                <span style="background: #fdf2f8; color: #be185d; font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 4px;">{badge_soft}</span>
            </div>
            <div style="font-size: 11px; color: #64748b; margin-bottom: 12px;">28% of skill ecosystem (Average 3.2 per profile)</div>
        ''', unsafe_allow_html=True)
        soft_palette = ["#10b981", "#7c3aed", "#ec4899", "#f59e0b", "#06b6d4", "#8b5cf6", "#14b8a6", "#f97316", "#3b82f6", "#6366f1"]
        for idx, item in enumerate(soft_items[:soft_limit]):
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

        if st.button(lbl_soft, key="btn_toggle_soft_skills", icon=icon_soft, icon_position="right"):
            st.session_state["top_soft_skills_limit"] = 10 if soft_limit == 6 else 6
            st.rerun()

def render_skills_distribution_by_category(skills_dist_data, unique_skills_count=None):
    """Render Ecosystem View: 100% Normalized Percentage Stacked Bar (Sesuai Gambar 1)."""
    # Menentukan angka unique skills secara dinamis dari database/filter yang aktif
    total_unique = (
        unique_skills_count
        or skills_dist_data.get("unique_skills_count")
        or skills_dist_data.get("total_skills_count", 2850)
    )

    st.markdown(f'''
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
            <div style="font-size: 13px; font-weight: 700; color: #0f172a;">Skills Distribution by Category</div>
            <span style="background: #f1f5f9; color: #475569; font-size: 10.5px; font-weight: 600; padding: 2px 6px; border-radius: 4px;">{total_unique:,} Total Skills</span>
        </div>
        <div style="font-size: 11px; color: #64748b; margin-bottom: 10px;">Segmented by industry taxonomy and technical depth</div>
    ''', unsafe_allow_html=True)

    cats = skills_dist_data.get("categories", [])
    categories_order = [
        "Tools & Software Platforms",
        "Business & Product Strategy",
        "Soft Skills & Leadership",
        "Technical & Engineering"
    ]

    # Palet warna persis seperti Gambar 1 (Blue, Teal/Green, Amber, Purple)
    subcat_colors = {
        # Technical & Engineering (Nuansa Biru)
        "Backend": "#1d4ed8",
        "Cloud": "#38bdf8",
        "Data": "#60a5fa",
        "Frontend & Web": "#2563eb",
        "Engineering Systems": "#818cf8",
        "Other Tech": "#93c5fd",

        # Soft Skills & Leadership (Nuansa Teal & Hijau)
        "Communication": "#0d9488",
        "Leadership": "#14b8a6",
        "Other Soft": "#99f6e4",
        "Problem Solving": "#10b981",

        # Business & Product Strategy (Nuansa Kuning, Oranye, Amber)
        "Business Analysis": "#fbbf24",
        "Product Owner": "#f59e0b",
        "Project Mgmt": "#d97706",

        # Tools & Software Platforms (Nuansa Ungu)
        "Dev Tools / IDEs": "#7c3aed",
        "Software Platforms": "#a855f7",
        "Design & Platform Tools": "#c084fc",
        "Git / Docker": "#7c3aed",
        "Jira / Agile": "#a855f7",
        "CI/CD Tools": "#c084fc"
    }

    all_subcats = set()
    for c in cats:
        all_subcats.update(c.get("subcategories", {}).keys())

    fig = go.Figure()

    # Normalisasi nilai menjadi 100% per kategori (persen)
    for subcat in sorted(list(all_subcats)):
        x_vals, y_vals, text_vals, hover_vals = [], [], [], []
        for cat_name in categories_order:
            row = next((c for c in cats if c["category"] == cat_name), None)
            sub_dict = row.get("subcategories", {}) if row else {}
            cat_total = sum(sub_dict.values())

            if row and subcat in sub_dict and cat_total > 0:
                cnt = sub_dict[subcat]
                pct = (cnt / cat_total) * 100
                x_vals.append(pct)
                y_vals.append(cat_name)
                # Tampilkan teks jika segmen cukup lebar (>= 5%)
                text_vals.append(f"{subcat} ({pct:.0f}%)" if pct >= 5 else "")
                hover_vals.append(f"<b>{cat_name}</b><br>{subcat}: {pct:.1f}% ({cnt:,} skills)<extra></extra>")
            else:
                x_vals.append(0)
                y_vals.append(cat_name)
                text_vals.append("")
                hover_vals.append("")

        fig.add_trace(go.Bar(
            y=y_vals,
            x=x_vals,
            name=subcat,
            orientation='h',
            marker=dict(
                color=subcat_colors.get(subcat, "#94a3b8"),
                line=dict(color='#ffffff', width=1.5)  # Garis pembatas putih antar segmen
            ),
            text=text_vals,
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(size=9.5, color='#0f172a', family='Inter, sans-serif'),
            hovertemplate=hover_vals
        ))

    fig.update_layout(
        barmode='stack',
        height=260,
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff"
    )

    # Kunci sumbu X dari 0% sampai 100%
    fig.update_xaxes(
        range=[0, 100],
        tickvals=[0, 25, 50, 75, 100],
        ticktext=["0%", "25%", "50%", "75%", "100%"],
        showgrid=True,
        gridcolor="#f1f5f9",
        tickfont=dict(size=8.5, color="#64748b")
    )
    fig.update_yaxes(
        tickfont=dict(size=9, color="#1e293b", weight="bold")
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown('''
        <div style="font-size: 11px; color: #64748b; margin-top: 4px;">
            Showing normalized percentage share within each category
        </div>
    </div>
    ''', unsafe_allow_html=True)