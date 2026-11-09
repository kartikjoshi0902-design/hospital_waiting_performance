"""
UI Design System & Enterprise Styling
======================================
Professional, publication-grade styling and visualization utilities
for the Hospital Patient Wait-Time & Capacity Optimizer.
Enforces strict equal-height alignment, column synchronization, and
clinical analytics dashboard layout standards.
"""

import streamlit as st
import plotly.graph_objects as go

# ─── Color Palette Tokens ─────────────────────────────────────────
COLORS = {
    "primary": "#1d4ed8",         # Deep Clinical Blue
    "primary_dark": "#1e3a8a",
    "primary_light": "#eff6ff",
    "secondary": "#0284c7",       # Sky Blue
    "accent": "#4f46e5",          # Indigo
    "success": "#059669",         # Emerald (Optimal/Stable)
    "success_light": "#ecfdf5",
    "success_border": "#a7f3d0",
    "warning": "#d97706",         # Amber (Near Capacity/Busy)
    "warning_light": "#fffbeb",
    "warning_border": "#fde68a",
    "danger": "#dc2626",          # Crimson (Bottleneck/Overloaded)
    "danger_light": "#fef2f2",
    "danger_border": "#fecaca",
    "slate_dark": "#0f172a",      # Headings & High Contrast Text
    "slate_body": "#334155",      # Body Text
    "slate_muted": "#64748b",     # Labels & Secondary Text
    "slate_border": "#e2e8f0",    # Card & Container Borders
    "slate_bg": "#f8fafc",        # Page Background
    "card_bg": "#ffffff",         # Card Surface
}


def inject_custom_css():
    """
    Injects enterprise-grade, clean light-mode dashboard CSS.
    Enforces strict flexbox equal-height column synchronization.
    """
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap');

        /* Global Typography & Canvas */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #0f172a;
            background-color: #f8fafc;
        }

        /* Streamlit Header / Footer Cleanup */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {
            background-color: transparent !important;
        }

        /* Page Layout Constraints */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3.5rem;
            max-width: 1320px;
        }

        /* Sidebar Enterprise Styling */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #e2e8f0 !important;
        }
        [data-testid="stSidebar"] hr {
            margin: 1.2rem 0;
            border-color: #f1f5f9;
        }
        [data-testid="stSidebar"] [data-testid="stSidebarNav"] span {
            font-weight: 500;
            font-size: 0.92rem;
            color: #334155 !important;
        }

        /* Executive Hero Banner */
        .executive-header {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 65%, #1e3a5f 100%);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 2rem 2.2rem;
            color: #ffffff;
            margin-bottom: 2rem;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
            position: relative;
            overflow: hidden;
        }
        .executive-tag {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 3px 10px;
            background: rgba(37, 99, 235, 0.22);
            border: 1px solid rgba(96, 165, 250, 0.35);
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: #93c5fd;
            margin-bottom: 0.8rem;
        }
        .executive-title {
            font-size: 2.1rem;
            font-weight: 800;
            color: #ffffff !important;
            margin: 0 0 0.45rem 0;
            letter-spacing: -0.02em;
            line-height: 1.25;
        }
        .executive-subtitle {
            font-size: 1.02rem;
            color: #cbd5e1 !important;
            margin: 0;
            max-width: 850px;
            line-height: 1.6;
        }

        /* =================================================================
           STRICT EQUAL-HEIGHT & SYNCHRONIZATION GRID RULES
           ================================================================= */

        /* Force all Streamlit column containers to stretch to full row height */
        div[data-testid="column"] {
            display: flex !important;
            flex-direction: column !important;
            flex: 1 1 0px !important;
        }

        div[data-testid="column"] > div {
            display: flex !important;
            flex-direction: column !important;
            flex: 1 1 100% !important;
            height: 100% !important;
        }

        div[data-testid="column"] > div > div[data-testid="stVerticalBlock"] {
            display: flex !important;
            flex-direction: column !important;
            flex: 1 1 100% !important;
            height: 100% !important;
        }

        div[data-testid="column"] > div > div[data-testid="stVerticalBlock"] > div[data-testid="stMarkdown"] {
            display: flex !important;
            flex-direction: column !important;
            flex: 1 1 100% !important;
            height: 100% !important;
        }

        div[data-testid="column"] > div > div[data-testid="stVerticalBlock"] > div[data-testid="stMarkdown"] > div {
            display: flex !important;
            flex-direction: column !important;
            flex: 1 1 100% !important;
            height: 100% !important;
        }

        /* 1. Synchronized Challenge / Bottleneck Cards */
        .challenge-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #dc2626;
            border-radius: 8px;
            padding: 1.25rem 1.15rem;
            height: 100% !important;
            min-height: 155px;
            display: flex !important;
            flex-direction: column !important;
            justify-content: flex-start !important;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
            box-sizing: border-box;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .challenge-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(15, 23, 42, 0.08);
        }
        .challenge-title {
            font-size: 0.96rem;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.35;
            margin-bottom: 0.45rem;
            min-height: 2.6rem; /* Exactly 2 lines so descriptions align on same baseline */
            display: flex;
            align-items: flex-start;
        }
        .challenge-desc {
            font-size: 0.85rem;
            color: #475569;
            line-height: 1.5;
            margin: 0;
            flex: 1 1 auto;
        }

        /* 2. Synchronized Methodology Cards */
        .method-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 1.6rem;
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
            box-sizing: border-box;
        }
        .method-card.blue-border {
            border-top: 4px solid #1d4ed8;
        }
        .method-card.green-border {
            border-top: 4px solid #059669;
        }
        .method-badge-container {
            min-height: 1.8rem;
            display: flex;
            align-items: center;
        }
        .method-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #0f172a;
            margin: 0.6rem 0 0.4rem 0;
            min-height: 3.2rem; /* Exactly 2 lines so paragraphs align on same baseline */
            display: flex;
            align-items: flex-start;
            line-height: 1.35;
        }
        .method-desc {
            color: #475569;
            font-size: 0.88rem;
            line-height: 1.55;
            min-height: 4.2rem; /* Synchronizes paragraph baseline before the formula container */
            margin: 0 0 0.8rem 0;
        }
        .formula-container {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 0.85rem 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            color: #1e293b;
            min-height: 5.2rem; /* Synchronizes formula box height */
            display: flex;
            flex-direction: column;
            justify-content: center;
            margin: 0 0 1rem 0;
        }
        .method-list {
            color: #475569;
            font-size: 0.85rem;
            line-height: 1.7;
            padding-left: 1.1rem;
            margin-bottom: 0;
            flex: 1 1 auto;
        }

        /* 3. Synchronized Workflow Cards */
        .workflow-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 1.35rem;
            height: 100% !important;
            min-height: 145px;
            display: flex !important;
            flex-direction: column !important;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
            box-sizing: border-box;
            margin-bottom: 0.6rem;
        }
        .workflow-step-tag {
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.35rem;
        }
        .workflow-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.45rem;
            min-height: 1.6rem;
        }
        .workflow-desc {
            color: #64748b;
            font-size: 0.86rem;
            line-height: 1.5;
            margin: 0;
            flex: 1 1 auto;
        }

        /* 4. Synchronized Metrics */
        [data-testid="stMetric"] {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            padding: 1.1rem 1.25rem !important;
            height: 100% !important;
            min-height: 120px !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: space-between !important;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
            box-sizing: border-box !important;
        }
        [data-testid="stMetricLabel"] p {
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            color: #64748b !important;
            text-transform: uppercase !important;
            letter-spacing: 0.04em !important;
        }
        [data-testid="stMetricValue"] div {
            font-size: 1.85rem !important;
            font-weight: 800 !important;
            color: #0f172a !important;
        }

        /* Enterprise Callouts */
        .pro-callout {
            border-radius: 8px;
            padding: 1rem 1.25rem;
            margin: 1.2rem 0;
            font-size: 0.92rem;
            line-height: 1.55;
            border: 1px solid transparent;
        }
        .pro-callout-info {
            background: #eff6ff;
            border-color: #bfdbfe;
            color: #1e40af;
        }
        .pro-callout-warning {
            background: #fffbeb;
            border-color: #fde68a;
            color: #92400e;
        }
        .pro-callout-danger {
            background: #fef2f2;
            border-color: #fecaca;
            color: #991b1b;
        }
        .pro-callout-success {
            background: #ecfdf5;
            border-color: #a7f3d0;
            color: #065f46;
        }

        /* Badges */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 3px 9px;
            border-radius: 6px;
            font-size: 0.74rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            text-transform: uppercase;
        }
        .status-badge-success {
            background: #ecfdf5;
            color: #047857;
            border: 1px solid #a7f3d0;
        }
        .status-badge-warning {
            background: #fffbeb;
            color: #b45309;
            border: 1px solid #fde68a;
        }
        .status-badge-danger {
            background: #fef2f2;
            color: #b91c1c;
            border: 1px solid #fecaca;
        }
        .status-badge-info {
            background: #eff6ff;
            color: #1d4ed8;
            border: 1px solid #bfdbfe;
        }

        /* Clean Table / DataFrame */
        [data-testid="stDataFrame"] {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
        }

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            background-color: #f1f5f9;
            padding: 4px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }
        .stTabs [data-baseweb="tab"] {
            height: 36px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.86rem;
            padding: 0 14px;
            color: #475569;
            border: none;
            background: transparent;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ffffff !important;
            color: #1d4ed8 !important;
            font-weight: 700 !important;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06) !important;
        }

        /* Status Dot */
        .status-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #10b981;
        }
    </style>
    """, unsafe_allow_html=True)


def render_header(title: str, subtitle: str, tag: str = "OPERATIONS RESEARCH PLATFORM", icon: str = None):
    """
    Renders an executive header banner with clean typography.
    """
    icon_html = f'<span style="margin-right: 8px;">{icon}</span>' if icon else ""
    st.markdown(f"""
    <div class="executive-header">
        <div class="executive-tag">
            <span class="status-indicator"></span>
            {tag}
        </div>
        <h1 class="executive-title">{icon_html}{title}</h1>
        <p class="executive-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar_branding():
    """
    Renders institutional branding in the sidebar.
    """
    with st.sidebar:
        st.markdown("""
        <div style="padding: 0.2rem 0 1rem 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 1.2rem;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="
                    width: 38px;
                    height: 38px;
                    background: #1d4ed8;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #ffffff;
                    font-weight: 800;
                    font-size: 16px;
                ">
                    OPD
                </div>
                <div>
                    <div style="font-weight: 800; font-size: 1.05rem; color: #0f172a; line-height: 1.2;">
                        Hospital Flow Analytics
                    </div>
                    <div style="font-size: 0.76rem; color: #64748b; font-weight: 500;">
                        Operations Research Platform
                    </div>
                </div>
            </div>
            <div style="margin-top: 0.85rem; display: flex; align-items: center; justify-content: space-between; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 10px; font-size: 0.78rem;">
                <span style="color: #64748b; font-weight: 500;">System Engine</span>
                <span style="color: #059669; font-weight: 700; display: inline-flex; align-items: center; gap: 5px;">
                    <span class="status-indicator"></span> Active
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def apply_plotly_theme(fig: go.Figure, height: int = 420) -> go.Figure:
    """
    Applies clean, publication-grade styling to Plotly figures.
    Uses muted colors, subtle gridlines, and clean typography.
    """
    fig.update_layout(
        template="plotly_white",
        font=dict(
            family="Inter, -apple-system, BlinkMacSystemFont, sans-serif",
            size=12,
            color="#334155"
        ),
        title=dict(
            font=dict(size=14, weight=700, color="#0f172a"),
            x=0.01,
            xanchor="left",
            yanchor="top"
        ),
        height=height,
        margin=dict(l=40, r=25, t=50, b=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            gridcolor="#f1f5f9",
            linecolor="#cbd5e1",
            tickfont=dict(size=11, color="#64748b"),
            title_font=dict(size=12, weight=600, color="#475569")
        ),
        yaxis=dict(
            gridcolor="#f1f5f9",
            linecolor="#cbd5e1",
            tickfont=dict(size=11, color="#64748b"),
            title_font=dict(size=12, weight=600, color="#475569")
        ),
        hoverlabel=dict(
            bgcolor="#0f172a",
            font_size=12,
            font_color="#ffffff",
            font_family="Inter, sans-serif",
            bordercolor="rgba(0,0,0,0)"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color="#475569")
        )
    )

    for trace in fig.data:
        if trace.type == "bar":
            try:
                trace.marker.cornerradius = 4
            except Exception:
                pass

    return fig
