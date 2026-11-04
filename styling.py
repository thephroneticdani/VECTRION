"""Shared visual tokens and VECTRION dark-purple Streamlit styling."""

COLORS = {
    "background": "#100D1C",
    "surface": "#191426",
    "surface_elevated": "#241B35",
    "primary": "#9B6DFF",
    "secondary": "#C5A4FF",
    "accent": "#E0C7FF",
    "text_primary": "#F4F0FA",
    "text_secondary": "#A99BBE",
    "border": "#382A4C",
    "success": "#55D6A6",
    "warning": "#F2BD68",
    "error": "#FF718B",
    "cyan": "#67E8F9",
    "magenta": "#D946EF",
    "purple_glow": "#9B6DFF66",
    "surface_input": "#171326",
    "surface_control": "#211A30",
    "surface_table_header": "#33234A",
    "button_start": "#7543D2",
    "button_end": "#8D3DA4",
    "white": "#FFFFFF",
}


def inject_global_styles(st):
    c = COLORS
    st.markdown(
        f"""
        <style>
        :root {{ --vx-bg:{c['background']}; --vx-surface:{c['surface']};
          --vx-raised:{c['surface_elevated']}; --vx-primary:{c['primary']};
          --vx-secondary:{c['secondary']}; --vx-text:{c['text_primary']};
          --vx-muted:{c['text_secondary']}; --vx-border:{c['border']}; }}
        .stApp {{ background: radial-gradient(ellipse at 12% 0%, {c['purple_glow']}, transparent 38%),
          radial-gradient(ellipse at 95% 18%, {c['magenta']}22, transparent 34%), var(--vx-bg) !important;
          color:var(--vx-text); }}
        html,body,[class*="css"] {{ font-family:Inter,"Segoe UI",Arial,sans-serif; }}
        h1,h2,h3 {{ font-family:"Space Grotesk",Outfit,"Segoe UI",sans-serif !important; }}
        [data-testid="stMetricValue"],.stNumberInput input {{ font-family:"JetBrains Mono",Consolas,monospace !important; }}
        h1 {{ color:var(--vx-text) !important; text-shadow:0 0 16px {c['purple_glow']}; letter-spacing:.2px; }}
        h2,h3 {{ color:{c['accent']} !important; }}
        p,label,[data-testid="stMarkdownContainer"] {{ color:var(--vx-text); }}
        [data-testid="stCaptionContainer"] {{ color:var(--vx-muted) !important; }}
        hr {{ border:0 !important; height:2px !important; background:linear-gradient(90deg,{c['primary']},{c['magenta']},{c['cyan']}) !important;
          box-shadow:0 0 10px {c['purple_glow']} !important; }}
        .stTextInput input,.stNumberInput input {{ background:{c['surface_input']} !important; color:var(--vx-text) !important;
          border:1px solid {c['border']} !important; border-radius:9px !important; }}
        [data-testid="stSelectbox"] [data-baseweb="select"] > div {{ background:{c['surface_control']} !important;
          color:var(--vx-text) !important; border:1px solid {c['border']} !important; border-radius:9px !important; }}
        [data-testid="stSelectbox"] [data-baseweb="select"] span {{ color:var(--vx-text) !important; }}
        [data-baseweb="popover"] > div,[data-baseweb="menu"] {{ background:var(--vx-surface) !important; border:1px solid var(--vx-primary) !important; }}
        [role="option"] {{ background:var(--vx-surface) !important; color:var(--vx-text) !important; }}
        .stButton > button,.stFormSubmitButton > button {{ background:linear-gradient(110deg,{c['button_start']},{c['button_end']}) !important;
          color:{c['white']} !important; border:1px solid {c['secondary']} !important; border-radius:9px !important; font-weight:600 !important;
          box-shadow:0 0 12px {c['purple_glow']} !important; }}
        .stButton > button:hover,.stFormSubmitButton > button:hover {{ border-color:{c['cyan']} !important; box-shadow:0 0 16px {c['purple_glow']} !important; }}
        [data-testid="stMetric"] {{ background:linear-gradient(135deg,var(--vx-raised),{c['surface_input']}) !important;
          border:1px solid {c['border']} !important; border-radius:13px !important; padding:13px !important; }}
        [data-testid="stMetricValue"] {{ color:{c['cyan']} !important; }}
        [data-testid="stTable"] {{ border:1px solid {c['border']} !important; border-radius:10px !important; overflow:auto !important; }}
        [data-testid="stTable"] th {{ background:{c['surface_table_header']} !important; color:{c['accent']} !important; }}
        [data-testid="stTable"] td {{ color:var(--vx-text) !important; }}
        [data-testid="stAlert"] {{ border-radius:10px; }}
        [class*="st-key-rekap-card-"] {{ background:linear-gradient(135deg,var(--vx-raised),var(--vx-surface)) !important;
          border:1px solid {c['border']} !important; border-radius:13px !important; padding:.35rem .55rem !important; margin-bottom:.55rem !important; }}
        *:focus-visible {{ outline:2px solid {c['cyan']} !important; outline-offset:2px; }}
        @media (max-width: 800px) {{ section.main > div {{ padding-left:1rem; padding-right:1rem; }} }}
        </style>
        """,
        unsafe_allow_html=True,
    )
