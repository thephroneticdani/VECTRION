"""Warm white, batik-accented VECTRION Streamlit styling."""

import base64


COLORS = {
    "background": "#FBFAF7",
    "surface": "#FFFFFF",
    "surface_elevated": "#F6F1E9",
    "primary": "#81583D",
    "secondary": "#B9845D",
    "accent": "#687858",
    "text_primary": "#332A23",
    "text_secondary": "#5C5046",
    "border": "#C8B7A3",
    "success": "#55765F",
    "warning": "#A97635",
    "error": "#A94F46",
    "cyan": "#637D70",
    "magenta": "#AD7E56",
    "purple_glow": "#B9845D22",
    "surface_input": "#FFFFFF",
    "surface_control": "#FFFFFF",
    "surface_table_header": "#F1EADF",
    "button_start": "#81583D",
    "button_end": "#A77553",
    "white": "#FFFFFF",
}


BATIK_KAWUNG_SVG = """<svg xmlns='http://www.w3.org/2000/svg' width='144' height='144' viewBox='0 0 144 144'>
<g fill='none' stroke='#81583D' stroke-width='1.15' stroke-opacity='.018'>
  <g transform='translate(36 36)'>
    <path d='M0-23 C-15-11-15 1 0 10 C15 1 15-11 0-23Z'/>
    <path d='M23 0 C11-15-1-15-10 0 C-1 15 11 15 23 0Z'/>
    <path d='M0 23 C15 11 15-1 0-10 C-15-1-15 11 0 23Z'/>
    <path d='M-23 0 C-11 15 1 15 10 0 C1-15-11-15-23 0Z'/>
    <circle r='3.5' fill='#81583D' fill-opacity='.02' stroke='none'/>
  </g>
  <g transform='translate(108 108)'>
    <path d='M0-23 C-15-11-15 1 0 10 C15 1 15-11 0-23Z'/>
    <path d='M23 0 C11-15-1-15-10 0 C-1 15 11 15 23 0Z'/>
    <path d='M0 23 C15 11 15-1 0-10 C-15-1-15 11 0 23Z'/>
    <path d='M-23 0 C-11 15 1 15 10 0 C1-15-11-15-23 0Z'/>
    <circle r='3.5' fill='#81583D' fill-opacity='.02' stroke='none'/>
  </g>
  <circle cx='108' cy='36' r='12'/>
  <circle cx='36' cy='108' r='12'/>
</g></svg>"""

BATIK_KAWUNG_DATA = base64.b64encode(BATIK_KAWUNG_SVG.encode("utf-8")).decode("ascii")
SIDEBAR_BATIK_SVG = BATIK_KAWUNG_SVG.replace("stroke-opacity='.018'", "stroke-opacity='.15'").replace("fill-opacity='.02'", "fill-opacity='.08'")
SIDEBAR_BATIK_DATA = base64.b64encode(SIDEBAR_BATIK_SVG.encode("utf-8")).decode("ascii")


def inject_global_styles(st, navigation_hidden=False):
    c = COLORS
    sidebar_visibility = 'section[data-testid="stSidebar"]{display:none !important;}' if navigation_hidden else ""
    mobile_bottom_padding = "2rem" if navigation_hidden else "8rem"
    st.markdown(
        f"""
        <style>
        :root {{
          --primary-color:{c['primary']} !important;
          --vx-bg:{c['background']}; --vx-surface:{c['surface']};
          --vx-raised:{c['surface_elevated']}; --vx-primary:{c['primary']};
          --vx-secondary:{c['secondary']}; --vx-accent:{c['accent']};
          --vx-text:{c['text_primary']}; --vx-muted:{c['text_secondary']};
          --vx-border:{c['border']};
        }}
        html, body, [class*="css"] {{
          font-family: Inter, "Segoe UI", Arial, sans-serif;
          color:var(--vx-text);
        }}
        p, [data-testid="stMarkdownContainer"] {{
          color:{c['text_primary']} !important; font-size:1rem; line-height:1.65;
        }}
        label, [data-testid="stWidgetLabel"] {{
          color:#30241B !important; font-weight:650 !important; font-size:.98rem !important;
        }}
        [data-testid="stCaptionContainer"] {{ color:#5C5046 !important; font-weight:500; }}
        [data-testid="stMainBlockContainer"] {{ max-width:1240px; padding-top:2rem; }}
        .stApp {{
          background-color:var(--vx-bg) !important;
          background-image:
            url("data:image/svg+xml;base64,{BATIK_KAWUNG_DATA}"),
            radial-gradient(ellipse at 5% 0%, #E8DCCB55, transparent 38%),
            radial-gradient(ellipse at 100% 100%, #DCE2D355, transparent 32%);
          background-repeat:repeat, no-repeat, no-repeat;
          background-size:240px 240px, auto, auto;
          background-attachment:fixed;
          color:var(--vx-text);
        }}
        [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
          background:transparent !important;
          color:var(--vx-text);
        }}
        section[data-testid="stSidebar"] > div:first-child {{
          position:relative;
          background-color:#F7F3ED !important;
          background-image:linear-gradient(180deg,#FBF8F2 0%,#F5EFE6 100%);
          border-right:1px solid {c['border']};
        }}
        section[data-testid="stSidebar"] > div:first-child::before,
        section[data-testid="stSidebar"] > div:first-child::after {{
          content:""; position:absolute; left:0; right:0; height:105px;
          pointer-events:none; opacity:.47; z-index:0;
          background-image:url("data:image/svg+xml;base64,{SIDEBAR_BATIK_DATA}");
          background-size:104px 104px; background-repeat:repeat-x;
          -webkit-mask-image:linear-gradient(to bottom,#000 5%,transparent 100%);
          mask-image:linear-gradient(to bottom,#000 5%,transparent 100%);
        }}
        section[data-testid="stSidebar"] > div:first-child::before {{ top:0; }}
        section[data-testid="stSidebar"] > div:first-child::after {{ bottom:0; transform:rotate(180deg); }}
        section[data-testid="stSidebar"] {{
          width:clamp(13rem,17vw,15.5rem) !important;
          min-width:13rem !important; max-width:15.5rem !important;
        }}
        section[data-testid="stSidebar"] > div:first-child {{
          width:100% !important; min-width:0 !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {{
          position:relative; z-index:1;
        }}
        {sidebar_visibility}
        header[data-testid="stHeader"] {{
          background:rgba(251,250,247,.96) !important;
          border-bottom:1px solid {c['border']};
          backdrop-filter:blur(8px);
        }}
        [data-testid="stToolbar"] {{ background:transparent !important; }}
        header[data-testid="stHeader"] button {{ color:{c['primary']} !important; }}
        header button[data-testid="stSidebarCollapseButton"],
        header button[data-testid="stSidebarExpandButton"] {{ display:none !important; }}
        h1,h2,h3 {{
          font-family:"Space Grotesk", Outfit, "Segoe UI", sans-serif !important;
          color:#63452F !important; font-weight:750 !important;
        }}
        h1 {{ letter-spacing:.1px; text-shadow:0 1px 0 #FFFFFF; font-size:2.5rem !important; }}
        h2 {{ font-size:1.8rem !important; }}
        h3 {{ font-size:1.35rem !important; }}
        [data-testid="stMetricValue"], .stNumberInput input {{
          font-family:"JetBrains Mono", Consolas, monospace !important;
        }}
        hr {{
          border:0 !important; height:2px !important;
          background:linear-gradient(90deg,{c['primary']},{c['secondary']},{c['accent']}) !important;
          box-shadow:0 1px 5px #81583D20 !important;
        }}
        .stTextInput input,.stNumberInput input {{
          background:{c['surface_input']} !important; color:var(--vx-text) !important;
          border:1.5px solid #9B7B5D !important; border-radius:9px !important;
          min-height:2.8rem; font-size:1rem !important; font-weight:550 !important;
          box-shadow:inset 0 1px 2px #3E30270D;
        }}
        .stTextInput input:focus,.stNumberInput input:focus {{
          border:2px solid {c['primary']} !important;
          box-shadow:0 0 0 3px #81583D24 !important;
        }}
        [data-testid="stSelectbox"] [data-baseweb="select"] > div {{
          background:{c['surface_control']} !important; color:var(--vx-text) !important;
          border:1.5px solid #9B7B5D !important; border-radius:9px !important;
          min-height:2.8rem; font-weight:550 !important;
        }}
        [data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within {{
          border:2px solid {c['primary']} !important; box-shadow:0 0 0 3px #81583D24 !important;
        }}
        [data-testid="stSelectbox"] [data-baseweb="select"] span {{ color:var(--vx-text) !important; }}
        [data-baseweb="popover"] > div,[data-baseweb="menu"] {{
          background:var(--vx-surface) !important; border:1px solid {c['secondary']} !important;
        }}
        [role="option"] {{ background:var(--vx-surface) !important; color:var(--vx-text) !important; }}
        [data-testid="stRadio"] input {{ accent-color:{c['primary']} !important; }}
        [data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {{
          border-color:{c['primary']} !important;
        }}
        [data-testid="stRadio"] [data-baseweb="radio"] input:checked + div {{
          border-color:{c['primary']} !important; background-color:{c['primary']} !important;
        }}
        [data-testid="stRadio"] [data-baseweb="radio"][aria-checked="true"] > div:first-child {{
          border-color:{c['primary']} !important; background-color:{c['primary']} !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:has([data-testid="stButton"]) [data-testid="stVerticalBlock"] {{
          display:flex !important; flex-direction:column !important; gap:.48rem !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stButton"] button {{
          min-height:3.4rem; padding:.55rem .8rem !important;
          justify-content:flex-start !important; text-align:left !important;
          border:1px solid #A98766 !important; border-radius:14px 7px 14px 7px !important;
          font-size:.94rem !important; font-weight:650 !important;
          white-space:normal !important; overflow-wrap:anywhere !important;
          box-shadow:0 2px 5px #49362912, inset 0 1px 0 #FFFFFF55 !important;
          transition:transform .16s ease, box-shadow .16s ease !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stButton"] button:hover {{
          transform:translateX(2px); box-shadow:0 4px 9px #49362920 !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stButton"] button[kind="secondary"] {{
          color:#523D2B !important; border-color:#CDB99F !important;
          background:linear-gradient(110deg,#FFFEFC,#F0E7DA) !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stButton"] button[kind="secondary"] * {{ color:#523D2B !important; }}
        section[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"] {{
          color:#FFF9F1 !important; border-color:#694930 !important;
          background:linear-gradient(115deg,#684A34,#9A704C) !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"],
        section[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"] * {{ color:#FFF9F1 !important; }}
        .stButton > button, .stButton > button * {{ color:#FFF9F1 !important; }}
        section[data-testid="stSidebar"] [data-testid="stButton"] button[aria-label^="⌂"] {{ border-radius:18px 8px 18px 8px !important; }}
        section[data-testid="stSidebar"] [data-testid="stButton"] button[aria-label^="▤"] {{ border-radius:7px !important; }}
        section[data-testid="stSidebar"] [data-testid="stButton"] button[aria-label^="⌁"] {{ border-radius:20px 7px 14px 7px !important; }}
        .stButton > button,.stFormSubmitButton > button {{
          background:linear-gradient(110deg,{c['button_start']},{c['button_end']}) !important;
          color:{c['white']} !important; border:1px solid {c['primary']} !important;
          border-radius:9px !important; font-weight:600 !important;
          box-shadow:0 2px 7px #81583D25 !important;
        }}
        .stButton > button *, .stFormSubmitButton > button * {{ color:#FFF9F1 !important; }}
        .stButton > button p, .stFormSubmitButton > button p {{ color:#FFF9F1 !important; }}
        section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] *,
        section[data-testid="stSidebar"] button[kind="secondary"] * {{ color:#523D2B !important; }}
        section[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] *,
        section[data-testid="stSidebar"] button[kind="primary"] * {{ color:#FFF9F1 !important; }}
        .stButton > button:hover,.stFormSubmitButton > button:hover {{
          border-color:{c['accent']} !important; box-shadow:0 3px 10px #81583D35 !important;
        }}
        [data-testid="stMetric"] {{
          background:linear-gradient(135deg,#FFFFFF,{c['surface_elevated']}) !important;
          border:1px solid {c['border']} !important; border-radius:13px !important;
          padding:13px !important; box-shadow:0 2px 10px #4937250A;
        }}
        [data-testid="stMetricValue"] {{ color:{c['primary']} !important; }}
        [data-testid="stTable"] {{
          background:#FFFFFF !important; border:1px solid {c['border']} !important;
          border-radius:10px !important; overflow:auto !important;
        }}
        [data-testid="stTable"] th {{ background:{c['surface_table_header']} !important; color:{c['primary']} !important; }}
        [data-testid="stTable"] td {{ color:var(--vx-text) !important; }}
        [data-testid="stAlert"] {{ border-radius:10px; }}
        .brand-logo img {{ display:block; height:auto; max-width:100%; }}
        .brand-logo-sidebar img {{ width:100%; max-width:230px; margin:0 auto; }}
        .brand-logo-hero img {{ width:100%; max-width:430px; margin:0 auto; }}
        [class*="st-key-recap-grid-"][class*="-header"] {{
          background:#F1EADF !important; border-top:1px solid #C8B7A3;
          border-bottom:1px solid #B79C7E; padding:.48rem .55rem !important;
        }}
        [class*="st-key-recap-grid-"][class*="-row-"] {{
          border-bottom:1px solid #E6DED4; padding:.42rem .55rem !important;
        }}
        [class*="st-key-recap-grid-"][class*="-row-"]:hover {{ background:#F7F3ED !important; }}
        [class*="st-key-recap-grid-"][class*="-row-"] [data-testid="stButton"] button {{
          min-height:2.1rem !important; padding:.3rem .45rem !important; font-size:.78rem !important;
          border-radius:6px !important; box-shadow:none !important;
        }}
        .vx-recap-header {{ color:#553B29; font-size:.82rem; font-weight:700; line-height:1.3; }}
        .vx-recap-cell {{ color:#332A23; font-size:.9rem; line-height:1.4; overflow-wrap:anywhere; }}
        *:focus-visible {{ outline:2px solid {c['accent']} !important; outline-offset:2px; }}
        @media (max-width: 800px) {{
          [data-testid="stMainBlockContainer"] {{ padding-left:1rem; padding-right:1rem; padding-top:1.25rem; padding-bottom:{mobile_bottom_padding}; }}
          h1 {{ font-size:2rem !important; }}
          h2 {{ font-size:1.5rem !important; }}
          .brand-logo-hero img {{ max-width:300px; }}
        }}
        @media (max-width: 768px) {{
          section[data-testid="stSidebar"] {{ min-width:0 !important; max-width:none !important; }}
          section[data-testid="stSidebar"] {{
            position:fixed !important; top:auto !important; bottom:0 !important; left:0 !important;
            width:100% !important; min-width:100% !important; max-width:100% !important;
            height:auto !important; max-height:132px !important; transform:none !important;
            z-index:1000 !important; box-shadow:0 -5px 22px #34261B20 !important;
            border-top:1px solid #B79C7E !important; overflow:visible !important;
          }}
          section[data-testid="stSidebar"] > div:first-child {{
            width:100% !important; height:auto !important; max-height:132px !important;
            padding:.35rem .55rem calc(.45rem + env(safe-area-inset-bottom)) !important;
            overflow:visible !important; background:#F7F3ED !important;
          }}
          section[data-testid="stSidebar"] > div:first-child::before {{ height:44px; opacity:.42; }}
          section[data-testid="stSidebar"] > div:first-child::after {{ height:30px; opacity:.3; }}
          section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
          section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {{ display:none !important; }}
          section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:not(:has([data-testid="stRadio"], [data-testid="stButton"])) {{ display:none !important; }}
          section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{ gap:.2rem !important; }}
          section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:has([data-testid="stButton"]) [data-testid="stVerticalBlock"] {{
            flex-direction:row !important; align-items:stretch !important; gap:.22rem !important;
          }}
          section[data-testid="stSidebar"] [data-testid="stButton"] {{ flex:1 1 0 !important; min-width:0 !important; }}
          section[data-testid="stSidebar"] [data-testid="stButton"] button {{
            min-height:3.4rem; height:auto !important; justify-content:center !important;
            text-align:center !important; padding:.28rem .1rem !important;
            font-size:.68rem !important; line-height:1.15 !important; border-radius:11px 5px 11px 5px !important;
          }}
          section[data-testid="stSidebar"] [data-testid="stButton"] button[aria-label^="▤"] {{ border-radius:5px !important; }}
          section[data-testid="stSidebar"] [data-testid="stButton"] button[aria-label^="⌁"] {{ border-radius:15px 5px 10px 5px !important; }}
          section[data-testid="stSidebar"] [data-testid="stRadio"] {{ margin:0 !important; }}
          section[data-testid="stSidebar"] [data-testid="stRadio"] > label {{ display:none !important; }}
          section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] {{
            display:flex !important; flex-direction:row !important; flex-wrap:nowrap !important;
            justify-content:center !important; align-items:center !important; gap:.3rem !important;
          }}
          section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"] {{
            display:flex !important; flex-direction:row !important; align-items:center !important;
            gap:.28rem !important; white-space:nowrap !important; padding:.38rem .5rem !important;
            border:1px solid #C8B7A3 !important; border-radius:999px !important;
            background:#FFFFFF !important; color:#493629 !important; font-size:.78rem !important;
          }}
          section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"][aria-checked="true"] {{
            background:#81583D !important; border-color:#63452F !important; color:#FFFFFF !important;
          }}
          section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"] > div:first-child {{
            width:0 !important; height:0 !important; opacity:0 !important; margin:0 !important;
          }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
