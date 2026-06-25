"""Branding, theme, and UI styling."""
from __future__ import annotations

from pathlib import Path

import streamlit as st
from PIL import Image

from config.settings import ASSETS_DIR

# Brand palette derived from enterprise election portal branding
COLORS = {
    "deep_blue": "#0a1628",
    "navy": "#1e3a8a",
    "gold": "#d4af37",
    "emerald": "#059669",
    "light_grey": "#94a3b8",
    "white": "#f8fafc",
    "glass": "rgba(255, 255, 255, 0.08)",
    "glass_border": "rgba(212, 175, 55, 0.25)",
}


def extract_logo_colors(logo_path: Path) -> dict:
    """Extract dominant colors from logo for dynamic theming."""
    try:
        img = Image.open(logo_path).convert("RGB")
        img = img.resize((50, 50))
        pixels = list(img.getdata())
        r = sum(p[0] for p in pixels) // len(pixels)
        g = sum(p[1] for p in pixels) // len(pixels)
        b = sum(p[2] for p in pixels) // len(pixels)
        return {"primary": f"#{r:02x}{g:02x}{b:02x}", "accent": COLORS["gold"]}
    except Exception:
        return {"primary": COLORS["navy"], "accent": COLORS["gold"]}


def get_logo_path() -> Path:
    for name in ("logo.png", "logo.jpg", "logo.jpeg", "logo.svg"):
        path = ASSETS_DIR / name
        if path.exists():
            return path
    return ASSETS_DIR / "logo.svg"


def inject_css(theme: str = "dark") -> None:
    is_dark = theme == "dark"
    bg = COLORS["deep_blue"] if is_dark else "#f1f5f9"
    text = COLORS["white"] if is_dark else "#0f172a"
    card_bg = "rgba(15, 23, 42, 0.75)" if is_dark else "rgba(255, 255, 255, 0.85)"
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background: linear-gradient(135deg, {bg} 0%, {'#1e293b' if is_dark else '#e2e8f0'} 50%, {bg} 100%);
            color: {text};
        }}

        .main-header {{
            background: linear-gradient(90deg, {COLORS['navy']} 0%, {COLORS['deep_blue']} 100%);
            border: 1px solid {COLORS['glass_border']};
            border-radius: 16px;
            padding: 1.5rem 2rem;
            margin-bottom: 1.5rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }}

        .main-header h1 {{
            color: {COLORS['gold']};
            font-weight: 800;
            margin: 0;
            font-size: 1.8rem;
        }}

        .main-header p {{
            color: {COLORS['light_grey']};
            margin: 0.25rem 0 0 0;
        }}

        .kpi-card {{
            background: {card_bg};
            border: 1px solid {COLORS['glass_border']};
            border-radius: 14px;
            padding: 1.25rem;
            backdrop-filter: blur(10px);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}

        .kpi-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(212, 175, 55, 0.15);
        }}

        .kpi-label {{
            color: {COLORS['light_grey']};
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 600;
        }}

        .kpi-value {{
            color: {COLORS['gold'] if is_dark else COLORS['navy']};
            font-size: 2rem;
            font-weight: 800;
            line-height: 1.2;
        }}

        .kpi-delta {{
            color: {COLORS['emerald']};
            font-size: 0.85rem;
            font-weight: 600;
        }}

        .insight-card {{
            background: linear-gradient(135deg, rgba(30,58,138,0.4) 0%, rgba(5,150,105,0.2) 100%);
            border-left: 4px solid {COLORS['gold']};
            border-radius: 0 12px 12px 0;
            padding: 1rem 1.25rem;
            margin: 0.5rem 0;
        }}

        .alert-badge {{
            background: {COLORS['gold']};
            color: {COLORS['deep_blue']};
            padding: 2px 8px;
            border-radius: 999px;
            font-size: 0.7rem;
            font-weight: 700;
        }}

        .login-container {{
            max-width: 420px;
            margin: 2rem auto;
            background: {card_bg};
            border: 1px solid {COLORS['glass_border']};
            border-radius: 20px;
            padding: 2.5rem;
            backdrop-filter: blur(16px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        }}

        .section-title {{
            color: {COLORS['gold']};
            font-weight: 700;
            font-size: 1.1rem;
            border-bottom: 2px solid {COLORS['glass_border']};
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }}

        div[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {COLORS['deep_blue']} 0%, #0f172a 100%);
            border-right: 1px solid {COLORS['glass_border']};
        }}

        .stButton > button {{
            background: linear-gradient(90deg, {COLORS['navy']}, {COLORS['emerald']});
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s;
        }}

        .stButton > button:hover {{
            box-shadow: 0 4px 20px rgba(5, 150, 105, 0.4);
            transform: scale(1.02);
        }}

        [data-testid="stMetricValue"] {{
            font-size: 1.8rem !important;
            font-weight: 800 !important;
        }}

        .progress-bar {{
            height: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            overflow: hidden;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, {COLORS['navy']}, {COLORS['gold']});
            border-radius: 4px;
            transition: width 0.5s ease;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_card(label: str, value: str, delta: str = "", icon: str = "") -> None:
    delta_html = f'<div class="kpi-delta">{delta}</div>' if delta else ""
    icon_html = f'<span style="font-size:1.2rem;margin-right:0.5rem;">{icon}</span>' if icon else ""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{icon_html}{label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header(title: str, subtitle: str = "") -> None:
    st.markdown(
        f"""
        <div class="main-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_progress(label: str, pct: float) -> None:
    st.markdown(f"**{label}** — {pct:.1f}%")
    st.markdown(
        f'<div class="progress-bar"><div class="progress-fill" style="width:{min(pct,100):.1f}%;"></div></div>',
        unsafe_allow_html=True,
    )


def show_logo(width: int = 180) -> None:
    logo_path = get_logo_path()
    if logo_path.exists() and logo_path.suffix.lower() != ".svg":
        st.image(str(logo_path), width=width)
    else:
        st.markdown(
            """
            <div style="text-align:center;padding:1rem;">
                <div style="font-size:2.5rem;font-weight:800;color:#d4af37;letter-spacing:-1px;">ERP™</div>
                <div style="font-size:0.7rem;color:#94a3b8;letter-spacing:0.2em;">ELECTION RESULTS PORTAL</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
