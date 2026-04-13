import streamlit as st
import plotly.graph_objects as go
import time
import os
import sys

# 加载多语言资源
from i18n import TRANSLATIONS, t, t_list

# 安全加载推理引擎 (避免 NumPy/torch 兼容性问题导致崩溃)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
epa_reasoning_engine = None
try:
    from reasoning_agents.policy_graph_agent import epa_reasoning_engine
except Exception:
    pass

# ==========================================
# 页面配置
# ==========================================
st.set_page_config(
    page_title="EuroPolicy Agent",
    page_icon="🇪🇺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# Google Stitch 设计系统 CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Google+Sans+Text:wght@400;500;700&family=Noto+Sans+SC:wght@400;500;700&display=swap');

    /* === 全局 Stitch 深色主题 === */
    html, body, [class*="css"], .stApp, .stMain, [data-testid="stAppViewContainer"] {
        font-family: 'Google Sans Text', 'Google Sans', 'Noto Sans SC', -apple-system, sans-serif !important;
        background-color: #191a1f !important;
        color: #e8eaed !important;
    }

    header[data-testid="stHeader"] { background: transparent !important; }
    footer { display: none !important; }
    .stDeployButton { display: none !important; }
    #MainMenu { display: none !important; }

    /* === 侧边栏 === */
    [data-testid="stSidebar"] {
        background-color: #1e1f25 !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
    }
    [data-testid="stSidebar"] * { color: #e8eaed !important; }
    [data-testid="stSidebar"] .stRadio label {
        border-radius: 24px !important;
        padding: 8px 16px !important;
        transition: background 0.2s ease !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,0.06) !important;
    }

    /* === 语言选择器样式 === */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: #e8eaed !important;
    }

    /* === Stitch 卡片系统 === */
    .stitch-card {
        background: #1e1f25;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 24px;
        padding: 32px;
        margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .stitch-card:hover {
        border-color: rgba(255,255,255,0.12);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }

    /* === 指标卡片 === */
    .metric-card {
        background: #1e1f25;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 20px;
        padding: 24px 28px;
        text-align: left;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        height: 180px; /* 强制固定高度，确保完全一致 */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-sizing: border-box;
    }
    .metric-card:hover {
        border-color: rgba(255,255,255,0.12);
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    }
    .metric-number {
        font-family: 'Google Sans', sans-serif;
        font-size: 2.5rem; /* 略微缩小以防止溢出 */
        font-weight: 700;
        line-height: 1;
        margin: 8px 0 8px 0;
        white-space: nowrap; /* 禁止数字换行 */
    }
    .metric-label-text {
        font-size: 0.75rem; /* 缩小标签字体 */
        font-weight: 500;
        color: #9aa0a6;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        width: 100%;
    }

    /* === 强制 Streamlit 列等高对齐 === */
    [data-testid="stHorizontalBlock"] {
        align-items: stretch !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        display: flex !important;
        flex-direction: column !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > div {
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] .metric-card,
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] .result-panel {
        flex: 1 !important;
    }

    /* === 品牌标题 === */
    .stitch-hero {
        font-family: 'Google Sans', 'Noto Sans SC', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        letter-spacing: -1.5px;
        line-height: 1.08;
        margin-bottom: 8px;
        background: linear-gradient(135deg, #8ab4f8 0%, #c58af9 50%, #f28b82 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .stitch-subtitle {
        font-size: 1.1rem;
        color: #9aa0a6;
        font-weight: 400;
        margin-bottom: 40px;
    }

    /* === 节标题 === */
    .section-title {
        font-family: 'Google Sans', 'Noto Sans SC', sans-serif;
        font-size: 1.5rem;
        font-weight: 500;
        color: #e8eaed;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* === Pill 标签 === */
    .stitch-pill { display:inline-block; background:rgba(138,180,248,0.12); color:#8ab4f8; border-radius:100px; padding:6px 16px; font-size:0.8rem; font-weight:500; white-space:nowrap; }
    .stitch-pill-green { display:inline-block; background:rgba(129,201,149,0.12); color:#81c995; border-radius:100px; padding:6px 16px; font-size:0.8rem; font-weight:500; white-space:nowrap; }
    .stitch-pill-red { display:inline-block; background:rgba(242,139,130,0.12); color:#f28b82; border-radius:100px; padding:6px 16px; font-size:0.8rem; font-weight:500; white-space:nowrap; }
    .stitch-pill-purple { display:inline-block; background:rgba(197,138,249,0.12); color:#c58af9; border-radius:100px; padding:6px 16px; font-size:0.8rem; font-weight:500; white-space:nowrap; }

    /* === 主按钮 === */
    .stButton > button {
        background: linear-gradient(135deg, #8ab4f8, #c58af9) !important;
        color: #1e1f25 !important;
        border: none !important;
        border-radius: 100px !important;
        padding: 12px 32px !important;
        font-family: 'Google Sans', 'Noto Sans SC', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 12px rgba(138,180,248,0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px rgba(138,180,248,0.5) !important;
    }

    /* === 输入框 === */
    .stTextArea textarea {
        background: #1e1f25 !important;
        color: #e8eaed !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 16px !important;
        font-family: 'Google Sans Text', 'Noto Sans SC', sans-serif !important;
    }
    .stTextArea textarea:focus {
        border-color: #8ab4f8 !important;
        box-shadow: 0 0 0 1px #8ab4f8 !important;
    }

    /* === 其他覆盖 === */
    .stAlert { border-radius: 16px !important; }
    .stPlotlyChart { border-radius: 16px; overflow: hidden; }

    /* === 结果面板 === */
    .result-panel {
        background: #1e1f25;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 20px;
        padding: 28px;
        margin-top: 16px;
        min-height: 240px;
        box-sizing: border-box;
    }
    .result-panel h4 { font-family: 'Google Sans', 'Noto Sans SC', sans-serif; color: #e8eaed; margin-bottom: 12px; }
    .result-text { color: #bdc1c6; font-size: 0.95rem; line-height: 1.7; white-space: pre-wrap; }

    /* === 活动卡片统一对齐 === */
    .activity-row {
        background: #1e1f25;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 24px;
        padding: 20px 28px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 20px;
        min-height: 72px;
        box-sizing: border-box;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .activity-row:hover {
        border-color: rgba(255,255,255,0.12);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .activity-date {
        color: #5f6368;
        font-size: 0.85rem;
        min-width: 100px;
        flex-shrink: 0;
    }
    .activity-title {
        flex: 1;
        font-size: 0.95rem;
        color: #e8eaed;
        line-height: 1.4;
    }
    .activity-tag {
        flex-shrink: 0;
    }

    /* === 图谱占位 === */
    .graph-placeholder {
        background: #1e1f25;
        border: 1px dashed rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 80px 40px;
        text-align: center;
        color: #5f6368;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 侧边栏
# ==========================================
with st.sidebar:
    # 语言选择器
    lang_options = {v["lang_label"]: k for k, v in TRANSLATIONS.items()}
    selected_lang_label = st.selectbox(
        "🌐",
        list(lang_options.keys()),
        index=0,
        label_visibility="collapsed"
    )
    lang = lang_options[selected_lang_label]

    st.markdown(f"""
    <div style="padding: 16px 0 12px 0;">
        <span style="font-size:2.5rem;">🇪🇺</span>
        <div style="font-family: 'Google Sans', 'Noto Sans SC', sans-serif; font-size: 1.4rem; font-weight: 700; margin-top: 8px; letter-spacing: -0.5px;">
            {t("sidebar_title", lang)}
        </div>
        <div style="font-size: 0.8rem; color: #9aa0a6; margin-top: 4px;">
            {t("sidebar_subtitle", lang)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    selected_module = st.radio(
        "Navigate",
        [t("nav_dashboard", lang), t("nav_copilot", lang), t("nav_graph", lang)],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown(f"""
    <div style="padding: 8px 0;">
        <span class="stitch-pill">{t("alpha_tag", lang)}</span>
    </div>
    <div style="font-size: 0.75rem; color: #5f6368; margin-top: 8px; line-height: 1.6;">
        {t("kb_version", lang)}<br>
        {t("scraper_label", lang)}<br>
        {t("parser_label", lang)}
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# Dashboard 页面
# ==========================================
if selected_module == t("nav_dashboard", lang):
    st.markdown(f'<div class="stitch-hero">{t("hero_title", lang)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stitch-subtitle">{t("hero_subtitle", lang)}</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4, gap="medium")
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label-text" title="{t("metric_directives", lang)}">{t("metric_directives", lang)}</div>
            <div class="metric-number" style="color:#8ab4f8;">1,204</div>
            <div><span class="stitch-pill">{t("metric_directives_tag", lang)}</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label-text" title="{t("metric_graph", lang)}">{t("metric_graph", lang)}</div>
            <div class="metric-number" style="color:#c58af9;">1.4M</div>
            <div><span class="stitch-pill-purple">{t("metric_graph_tag", lang)}</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label-text" title="{t("metric_obligations", lang)}">{t("metric_obligations", lang)}</div>
            <div class="metric-number" style="color:#f28b82;">42</div>
            <div><span class="stitch-pill-red">{t("metric_obligations_tag", lang)}</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label-text" title="{t("metric_risks", lang)}">{t("metric_risks", lang)}</div>
            <div class="metric-number" style="color:#81c995;">7</div>
            <div><span class="stitch-pill-green">{t("metric_risks_tag", lang)}</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 热力图
    st.markdown(f'<div class="section-title">{t("heatmap_title", lang)}</div>', unsafe_allow_html=True)
    fig = go.Figure(data=go.Heatmap(
        z=[[82, 15, 45, 68, 12], [35, 8, 72, 91, 55], [60, 78, 20, 5, 30]],
        x=t_list("heatmap_x", lang),
        y=t_list("heatmap_y", lang),
        colorscale=[[0, '#1e1f25'], [0.5, '#8ab4f8'], [1, '#c58af9']],
        hovertemplate='%{x}<br>%{y}<br>Score: %{z}<extra></extra>'
    ))
    fig.update_layout(
        height=340, template="plotly_dark",
        paper_bgcolor='#1e1f25', plot_bgcolor='#1e1f25',
        margin=dict(l=0, r=0, t=16, b=0),
        font=dict(family="Google Sans, Noto Sans SC, sans-serif", color="#9aa0a6"),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig, use_container_width=True)

    # 动态
    st.markdown(f'<div class="section-title">{t("recent_title", lang)}</div>', unsafe_allow_html=True)
    activities = t_list("activities", lang)
    tag_classes = ["stitch-pill-red", "stitch-pill", "stitch-pill-purple"]
    for i, act in enumerate(activities):
        tc = tag_classes[i % len(tag_classes)]
        st.markdown(f"""
        <div class="activity-row">
            <div class="activity-date">{act["date"]}</div>
            <div class="activity-title">{act["title"]}</div>
            <span class="activity-tag {tc}" style="font-size:0.75rem;">{act["tag_text"]}</span>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# Copilot 页面
# ==========================================
elif selected_module == t("nav_copilot", lang):
    st.markdown(f'<div class="stitch-hero">{t("copilot_hero", lang)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stitch-subtitle">{t("copilot_subtitle", lang)}</div>', unsafe_allow_html=True)

    hints = t_list("copilot_hints", lang)
    st.markdown(f"""
    <div class="stitch-card" style="padding:20px 28px;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
            <span style="font-size:1.2rem;">💡</span>
            <span style="font-weight:500; color:#8ab4f8;">{t("copilot_hint_title", lang)}</span>
        </div>
        <div style="color:#9aa0a6; font-size:0.9rem; line-height:1.8;">
            {"<br>".join(hints)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    query = st.text_area("Query:", value=t("copilot_default_query", lang), height=120, label_visibility="collapsed")

    if st.button(t("copilot_button", lang), type="primary"):
        with st.status(t("copilot_status", lang), expanded=True) as status:
            st.write(t("copilot_step1", lang)); time.sleep(0.8)
            st.write(t("copilot_step2", lang)); time.sleep(0.8)
            st.write(t("copilot_step3", lang)); time.sleep(0.6)

            legal_result, sales_result = "", ""
            if epa_reasoning_engine:
                init_state = {"query": query, "graph_context": "", "legal_analysis": "", "sales_strategy": ""}
                for state_update in epa_reasoning_engine.stream(init_state):
                    pass
                legal_result = state_update.get("legal_expert", {}).get("legal_analysis", "")
                sales_result = state_update.get("sales_strategist", {}).get("sales_strategy", "")
            if not legal_result: legal_result = t("copilot_legal_fallback", lang)
            if not sales_result: sales_result = t("copilot_sales_fallback", lang)

            status.update(label=t("copilot_done", lang), state="complete", expanded=False)

        col_a, col_b = st.columns(2, gap="medium")
        with col_a:
            st.markdown(f"""
            <div class="result-panel">
                <h4>{ t("copilot_legal_title", lang) }</h4>
                <span class="stitch-pill-red" style="margin-bottom:12px;">{ t("copilot_legal_tag", lang) }</span>
                <div class="result-text">{legal_result}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
            <div class="result-panel">
                <h4>{ t("copilot_sales_title", lang) }</h4>
                <span class="stitch-pill-green" style="margin-bottom:12px;">{ t("copilot_sales_tag", lang) }</span>
                <div class="result-text">{sales_result}</div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# Knowledge Graph 页面
# ==========================================
elif selected_module == t("nav_graph", lang):
    st.markdown(f'<div class="stitch-hero">{t("graph_hero", lang)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stitch-subtitle">{t("graph_subtitle", lang)}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown(f"""<div class="metric-card"><div class="metric-label-text" title="{t("graph_metric_dir", lang)}">{t("graph_metric_dir", lang)}</div><div class="metric-number" style="color:#8ab4f8;">2,847</div><div></div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card"><div class="metric-label-text" title="{t("graph_metric_art", lang)}">{t("graph_metric_art", lang)}</div><div class="metric-number" style="color:#c58af9;">18,392</div><div></div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card"><div class="metric-label-text" title="{t("graph_metric_ref", lang)}">{t("graph_metric_ref", lang)}</div><div class="metric-number" style="color:#81c995;">42,156</div><div></div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="graph-placeholder">
        <div style="font-size:3rem; margin-bottom:16px; opacity:0.4;">🕸️</div>
        <div style="font-size: 1.1rem; color: #9aa0a6; margin-bottom: 8px;">{t("graph_placeholder_title", lang)}</div>
        <div style="font-size: 0.85rem; color: #5f6368; max-width: 500px; margin: 0 auto; line-height: 1.6;">
            {t("graph_placeholder_desc", lang)}<br>
            <code style="color:#8ab4f8;">(Directive)-[:REFERENCES]->(Directive)</code><br>
            <code style="color:#c58af9;">(Directive)-[:HAS_ARTICLE]->(Article)</code>
        </div>
    </div>
    """, unsafe_allow_html=True)
