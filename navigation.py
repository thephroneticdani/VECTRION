"""Small, testable helpers for page state and cross-page recap persistence."""


PAGES = ("Beranda", "Pra-Desain", "Pasca-ETABS", "Pasca-ETABS-Balok", "Pasca-ETABS-Kolom")


def initialize_state(state):
    defaults = {
        "halaman": "Beranda",
        "draft_balok": None,
        "rekap_balok": {},
        "rekap_pelat": {},
        "rekap_kolom": {},
        "draft_pelat": None,
        "etabs_beam_summary": None,
        "rekap_etabs_balok": {},
        "rekap_analisis_etabs": {},
        "show_etabs_rebar": False,
    }
    for key, value in defaults.items():
        if key not in state:
            state[key] = value.copy() if isinstance(value, dict) else value


def navigate(state, page):
    if page not in PAGES:
        raise ValueError(f"Halaman tidak dikenal: {page}")
    state["halaman"] = page
