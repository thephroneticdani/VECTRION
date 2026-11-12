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


def inject_global_styles(st, navigation_hidden=False, theme="Terang", homepage=False):
    # Infer the page from session state so older call sites remain compatible.
    homepage = homepage or st.session_state.get("halaman") == "Beranda"
    c = COLORS
    sidebar_visibility = 'section[data-testid="stSidebar"]{display:none !important;}' if navigation_hidden else ""
    mobile_bottom_padding = "2rem" if navigation_hidden else "8rem"
    dark_theme_css = """html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background-color:#111820!important;color:#e8edf2!important}
      .stApp{background-image:radial-gradient(ellipse at 5% 0%,#26313c55,transparent 38%),radial-gradient(ellipse at 100% 100%,#27342d55,transparent 32%)!important}
      p,[data-testid="stMarkdownContainer"],label,[data-testid="stWidgetLabel"],h1,h2,h3,[data-testid="stCaptionContainer"]{color:#e8edf2!important;text-shadow:none!important}
      header[data-testid="stHeader"]{background:rgba(17,24,32,.96)!important;border-color:#394550!important}
      section[data-testid="stSidebar"]>div:first-child{background:#19222c!important;background-image:linear-gradient(180deg,#202b36,#151d26)!important;border-color:#394550!important}
      .stTextInput input,.stNumberInput input,[data-testid="stSelectbox"] [data-baseweb="select"]>div,[data-baseweb="popover"]>div,[data-baseweb="menu"],[role="option"]{background:#202b36!important;color:#e8edf2!important;border-color:#526170!important}
      [data-testid="stMetric"]{background:linear-gradient(135deg,#202b36,#283440)!important;border-color:#465461!important}
      [data-testid="stMetricValue"]{color:#d8ad86!important}
      [data-testid="stTable"]{background:#202b36!important;border-color:#465461!important}
      [data-testid="stTable"] th{background:#2e3b47!important;color:#f0d7c0!important}[data-testid="stTable"] td{color:#e8edf2!important}
      .brand-logo img{filter:brightness(1.28) saturate(1.25) drop-shadow(0 0 5px #f4c783bb) drop-shadow(0 0 14px #c78c50aa)}
      section[data-testid="stSidebar"] [data-testid="stButton"] button[kind="secondary"]{background:#25313d!important;color:#e8edf2!important;border-color:#526170!important}
      section[data-testid="stSidebar"] [data-testid="stButton"] button[kind="secondary"] *{color:#e8edf2!important}
      .vx-recap-table{color:#e8edf2;background:#202b36;border-color:#526170}
      .vx-recap-table th{background:#2e3b47;color:#f0d7c0;border-color:#526170}
      .vx-recap-table td{border-color:#394957}.vx-recap-table tbody tr:nth-child(even){background:#25313d}
      .vx-recap-mobile-label{color:#e0b890}
      @media(max-width:768px){section[data-testid="stSidebar"]>div:first-child{background:#19222c!important}.vx-recap-table tbody tr{background:#202b36;border-color:#526170;box-shadow:none}.vx-recap-table td{border-color:#394957}}
    """ if theme in ("Gelap", "Futuristik") else ""
    if theme == "Futuristik":
        hero_theme_css = """[class*="st-key-home-hero"]{background:transparent!important;border-color:transparent}
          [class*="st-key-home-hero"] [data-testid="stColumn"]{background:rgba(7,12,29,.8);border-color:#20e6ff99;color:#f5f4ff;box-shadow:0 0 28px #07cde833,inset 0 0 18px #bd35ff12}
          [class*="st-key-home-hero"] h2{color:#47efff!important;text-shadow:0 0 12px #08cfff99!important}
          [class*="st-key-home-hero"] p,[class*="st-key-home-hero"] [data-testid="stCaptionContainer"]{color:#eeeaff!important;text-shadow:0 0 8px #ca36ff66!important}
      [class*="st-key-home-hero"] .brand-logo-hero img{filter:brightness(1.18) contrast(1.12) saturate(1.35) drop-shadow(0 0 5px #18eaff) drop-shadow(0 0 14px #d63dffcc)!important}
        """
    elif theme == "Gelap":
        hero_theme_css = """[class*="st-key-home-hero"]{background:transparent!important;border-color:transparent}
      [class*="st-key-home-hero"] [data-testid="stColumn"]{background:rgba(17,24,32,.8);border-color:#81909f99;color:#e8edf2}
      [class*="st-key-home-hero"] h2,[class*="st-key-home-hero"] p,[class*="st-key-home-hero"] [data-testid="stCaptionContainer"]{color:#e8edf2!important;text-shadow:none!important}
      [class*="st-key-home-hero"] .brand-logo-hero img{filter:brightness(1.28) contrast(1.1) saturate(1.25) drop-shadow(0 0 5px #f4c783bb) drop-shadow(0 0 14px #c78c50aa)}
        """
    else:
        hero_theme_css = """[class*="st-key-home-hero"]{background:transparent!important;border-color:transparent}
      [class*="st-key-home-hero"] [data-testid="stColumn"]{background:rgba(251,250,247,.8);border-color:#81583d66;color:#332a23}
      [class*="st-key-home-hero"] h2{color:#63452f!important;text-shadow:none!important}
      [class*="st-key-home-hero"] p{color:#332a23!important;text-shadow:none!important}
      [class*="st-key-home-hero"] [data-testid="stCaptionContainer"]{color:#5c5046!important;text-shadow:none!important}
        """
    page_surface = {"Gelap": "rgba(17,24,32,.8)", "Futuristik": "rgba(7,12,29,.8)"}.get(theme, "rgba(251,250,247,.8)")
    navigation_surface = {"Gelap": "rgba(17,24,32,.85)", "Futuristik": "rgba(8,12,29,.9)"}.get(theme, "rgba(251,250,247,.85)")
    page_border = {"Gelap": "#81909f99", "Futuristik": "#22ddff88"}.get(theme, "#81583d55")
    page_fallback = {"Gelap": "#111820", "Futuristik": "#080b18"}.get(theme, "#FBFAF7")
    alert_surface = {"Gelap": "rgba(52,49,31,.8)", "Futuristik": "rgba(17,22,43,.8)"}.get(theme, "rgba(255,248,213,.8)")
    page_overlay = {"Gelap": ".24", "Futuristik": ".2"}.get(theme, ".16")
    homepage_css = f""".stApp{{position:relative;isolation:isolate;background:{page_fallback}!important;background-image:none!important}}
      html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"],[data-testid="stMainBlockContainer"]{{background:transparent!important}}
      [data-testid="stAppViewContainer"]{{position:relative}}
      header[data-testid="stHeader"]{{background:{page_surface}!important;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}}
      section[data-testid="stSidebar"]>div:first-child{{background:{navigation_surface}!important;background-image:none!important;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}}
      [data-testid="stMainBlockContainer"] [class*="st-key-page-title"],[data-testid="stMainBlockContainer"] [class*="st-key-recap-section"]{{background:{page_surface};border:1px solid {page_border};border-radius:16px;padding:1rem;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}}
      [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"]:has(>[data-testid="stElementContainer"] h3){{background:{page_surface}!important;border-color:{page_border}!important;border-radius:14px;padding:1rem;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}}
      [data-testid="stMainBlockContainer"] [data-testid="stAlert"]{{background:{alert_surface}!important;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}}
      [data-testid="stMainBlockContainer"] .element-container:has(.vx-site-video-layer){{position:static!important;height:0!important;margin:0!important;padding:0!important}}
      .vx-site-video-layer{{position:fixed;inset:0;width:100vw;height:100vh;height:100dvh;z-index:-1;overflow:hidden;pointer-events:none}}
      .vx-site-video-layer video{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center}}
      .vx-site-video-shade{{position:absolute;inset:0;background:linear-gradient(120deg,rgba(10,16,23,{page_overlay}),rgba(10,16,23,.08))}}
      @media(prefers-reduced-motion:reduce){{.vx-site-video-layer video{{display:none}}}}
    """ if homepage else ""
    futuristic_css = """
      @keyframes vx-neon-drift{0%{background-position:0% 40%}50%{background-position:100% 60%}100%{background-position:0% 40%}}
      :root{--primary-color:#10cfe8!important;--vx-bg:#080b18;--vx-surface:#10172b;--vx-raised:#17152e;--vx-primary:#13d9f2;--vx-text:#f5f4ff;--vx-border:#26d9f277}
      .stApp:not(:has(.vx-site-video-layer)){color:#f5f4ff!important;background-color:#080b18!important;background-image:linear-gradient(125deg,#080b18,#0b1830,#21102f,#081b29)!important;background-size:300% 300%!important;animation:vx-neon-drift 18s ease infinite}
      html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{color:#f5f4ff!important}
      h1,h2,h3,h4,[data-testid="stMetricValue"]{color:#48eaff!important;text-shadow:0 0 10px #14dfff70,0 0 24px #b637ff44!important}
      .brand-logo img{filter:brightness(1.18) saturate(1.35) drop-shadow(0 0 5px #18eaff) drop-shadow(0 0 14px #d63dffcc)!important}
      p,label,[data-testid="stMarkdownContainer"],[data-testid="stWidgetLabel"],[data-testid="stCaptionContainer"]{color:#e8e8fa!important}
      header[data-testid="stHeader"],section[data-testid="stSidebar"]>div:first-child{background:rgba(8,12,29,.9)!important;border-color:#20ddff77!important;backdrop-filter:blur(16px)}
      section[data-testid="stSidebar"] [data-testid="stButton"] button{background:linear-gradient(120deg,#121b31,#21132f)!important;color:#e9faff!important;border-color:#1bd9ed88!important;box-shadow:0 0 12px #08d3e822}
      section[data-testid="stSidebar"] [data-testid="stButton"] button:hover{border-color:#ed49f8!important;box-shadow:0 0 18px #db35ff66}
      [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"]:has(>[data-testid="stElementContainer"] h3){background:rgba(8,12,29,.8)!important;border:1px solid #24d8ee77!important;border-radius:18px!important;padding:1.5rem!important;margin:.75rem 0 1.35rem!important;box-shadow:0 0 28px #0ad7eb36,0 0 44px #db35ff18,inset 0 0 18px #0ad7eb0d}
      [data-testid="stMainBlockContainer"] [class*="st-key-page-title"],[data-testid="stMainBlockContainer"] [class*="st-key-recap-section"]{background:rgba(8,12,29,.8)!important;border-color:#26ddf077!important;padding:1.5rem!important;box-shadow:0 0 28px #0ad7eb36,0 0 44px #db35ff18}
      [data-testid="stMainBlockContainer"] [data-testid="stAlert"]{color:#f4efff!important;border:1px solid #cc4cff99!important;box-shadow:0 0 18px #c43bff22}
      .vx-site-video-shade{background:linear-gradient(120deg,#07102133,#05283422,#30104133,#07102122)!important;background-size:300% 300%!important;animation:vx-neon-drift 18s ease infinite}
      [data-testid="stMainBlockContainer"] .stButton button{background:linear-gradient(105deg,#0c5065,#542565)!important;color:#fff!important;border:1px solid #30eaff99!important;box-shadow:0 0 12px #07cde833}
      [data-testid="stMainBlockContainer"] input,[data-testid="stMainBlockContainer"] [data-baseweb="select"]>div{background:#111a30!important;color:#f5f4ff!important;border-color:#27dff277!important}
      @media(prefers-reduced-motion:reduce){.stApp,.vx-site-video-shade{animation:none!important}}
    """ if theme == "Futuristik" else ""
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
        .vx-recap-table-wrap {{ width:100%; max-width:100%; margin:.55rem 0 1rem; }}
        .vx-recap-table {{
          width:100%; table-layout:auto; border-collapse:separate; border-spacing:0;
          border:1.5px solid #A9896B; border-radius:8px; overflow:hidden;
          color:#332A23; background:#FFFCF7; font-size:.94rem;
        }}
        .vx-recap-table th {{
          padding:.72rem .68rem; background:#F1EADF; color:#553B29;
          border-bottom:2px solid #9C7658; text-align:left; vertical-align:middle;
          font-size:.91rem; font-weight:750; line-height:1.35; overflow-wrap:anywhere;
        }}
        .vx-recap-table td {{
          padding:.68rem; border-bottom:1px solid #DCCDBD; vertical-align:top;
          line-height:1.45; overflow-wrap:anywhere; word-break:normal;
        }}
        .vx-recap-table tbody tr:last-child td {{ border-bottom:0; }}
        .vx-recap-table tbody tr:nth-child(even) {{ background:#F9F5EF; }}
        .vx-recap-mobile-label {{ display:none; }}
        .vx-recap-value {{ display:block; min-width:0; overflow-wrap:anywhere; }}
        [class*="st-key-recap-actions-"] {{ display:flex; flex-wrap:wrap; gap:.4rem; margin-top:-.4rem; }}
        [class*="st-key-recap-actions-"] [data-testid="stButton"] button {{
          width:auto !important; min-height:2rem; padding:.32rem .65rem !important;
          border-radius:6px !important; font-size:.8rem !important; box-shadow:none !important;
        }}
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
          section[data-testid="stSidebar"] [class*="st-key-post-etabs-module-navigation"] [data-testid="stHorizontalBlock"] {{
            display:grid !important; grid-template-columns:minmax(0, 1fr) minmax(0, 1fr) !important;
            width:100% !important; max-width:100% !important; box-sizing:border-box !important;
            align-items:stretch !important; gap:.45rem !important;
          }}
          section[data-testid="stSidebar"] [class*="st-key-post-etabs-module-navigation"] [data-testid="column"] {{
            width:100% !important; min-width:0 !important; max-width:100% !important;
            flex:initial !important; box-sizing:border-box !important;
          }}
          section[data-testid="stSidebar"] [class*="st-key-post-etabs-module-navigation"] [data-testid="stButton"] {{
            width:100% !important; min-width:0 !important; max-width:100% !important;
          }}
          section[data-testid="stSidebar"] [class*="st-key-post-etabs-module-navigation"] [data-testid="stButton"] button {{
            display:flex !important; width:100% !important; min-width:0 !important; max-width:100% !important;
            box-sizing:border-box !important; white-space:nowrap !important; overflow:hidden !important;
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
          .vx-recap-mobile-label {{
            display:block; color:#63472F; font-size:.83rem; font-weight:700;
            line-height:1.4; overflow-wrap:anywhere;
          }}
          .vx-recap-table-wrap {{ margin:.5rem 0 .65rem; }}
          .vx-recap-table {{ border:0; border-radius:0; background:transparent; font-size:.9rem; }}
          .vx-recap-table thead {{ display:none; }}
          .vx-recap-table, .vx-recap-table tbody, .vx-recap-table tr {{ display:block; width:100%; }}
          .vx-recap-table tbody tr {{
            margin:0 0 .8rem; padding:.35rem .72rem; border:1.5px solid #A9896B;
            border-radius:9px; background:#FFFCF7; box-shadow:0 2px 7px #4937250D;
          }}
          .vx-recap-table td {{
            display:grid; grid-template-columns:minmax(7rem, 41%) minmax(0, 1fr);
            align-items:start; gap:.6rem; padding:.46rem 0;
            border-bottom:1px solid #E6DED4; text-align:left;
          }}
          .vx-recap-table td:last-child {{ border-bottom:0; }}
          .vx-recap-value {{ text-align:right; font-size:.89rem; }}
          [class*="st-key-recap-actions-"] {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(9rem, 1fr)); gap:.45rem; margin:.1rem 0 .9rem; }}
          [class*="st-key-recap-actions-"] [data-testid="stButton"] button {{ width:100% !important; }}
        }}
        {dark_theme_css}
        {homepage_css}
        {futuristic_css}
        [class*="st-key-home-hero"] {{ position:relative; min-height:20rem; padding:0 !important; overflow:hidden; border:1px solid #FFFFFF48; border-radius:18px; background:#F6F1E9; isolation:isolate; }}
        [class*="st-key-home-hero"][data-testid="stVerticalBlock"] {{ position:relative; z-index:1; min-height:17rem; justify-content:center; }}
        [class*="st-key-home-hero"] .element-container:has(.vx-home-video-layer) {{ position:absolute !important; inset:0 !important; width:100% !important; height:100% !important; z-index:0; }}
        [class*="st-key-home-hero"] .vx-home-video-layer {{ position:absolute; inset:0; width:100%; height:100%; z-index:0; overflow:hidden; pointer-events:none; }}
        [class*="st-key-home-hero"] .vx-home-video-layer video {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:center 55%; }}
        [class*="st-key-home-hero"] .vx-home-video-shade {{ position:absolute; inset:0; background:linear-gradient(120deg,rgba(12,19,27,.24),rgba(12,19,27,.12)),linear-gradient(0deg,rgba(12,19,27,.2),transparent 70%); }}
        [class*="st-key-home-hero"] [data-testid="stHorizontalBlock"] {{ padding:1rem; }}
        [class*="st-key-home-hero"] [data-testid="stColumn"] {{ min-height:17rem; padding:1.5rem 1.6rem; border:1px solid; border-radius:16px; backdrop-filter:blur(12px) saturate(120%); -webkit-backdrop-filter:blur(12px) saturate(120%); }}
        [class*="st-key-home-hero"] [data-testid="stColumn"]:has(.brand-logo-hero) {{ display:flex; align-items:center; justify-content:center; }}
        @media(max-width:768px) {{ [class*="st-key-home-hero"] {{ min-height:22rem; }} [class*="st-key-home-hero"][data-testid="stVerticalBlock"] {{ min-height:21rem; }} [class*="st-key-home-hero"] [data-testid="stHorizontalBlock"] {{ padding:1rem; }} [class*="st-key-home-hero"] [data-testid="stColumn"] {{ min-height:16rem; padding:1rem 1.2rem; }} [class*="st-key-home-hero"] [data-testid="stColumn"]:has(.brand-logo-hero) {{ display:none !important; }} [class*="st-key-home-hero"] .vx-home-video-layer video {{ object-position:58% center; }} }}
        @media(prefers-reduced-motion:reduce) {{ [class*="st-key-home-hero"] .vx-home-video-layer video {{ display:none; }} }}
        {hero_theme_css}
        </style>
        """,
        unsafe_allow_html=True,
    )
