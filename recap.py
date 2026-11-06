"""Presentation helpers for saved recap entries; no engineering calculations."""


BEAM_RATIO_MIN = 0.5
BEAM_RATIO_MAX = 0.6667
_RATIO_TOLERANCE = 1e-9


def _mm(value):
    return f"{float(value):g}"


def beam_recap_warnings(data):
    """Return independent warning messages for a saved beam recap entry."""
    warnings = []
    selected_height = float(data["Tinggi pilihan (mm)"])
    minimum_height = float(data["Tinggi minimum (mm)"])
    width = float(data["Lebar pilihan (mm)"])

    if selected_height < minimum_height:
        warnings.append(
            f"Peringatan: Tinggi pilihan {_mm(selected_height)} mm < "
            f"tinggi minimum {_mm(minimum_height)} mm."
        )
    if selected_height > 0:
        ratio = width / selected_height
        if (
            ratio < BEAM_RATIO_MIN - _RATIO_TOLERANCE
            or ratio > BEAM_RATIO_MAX + _RATIO_TOLERANCE
        ):
            warnings.append(
                f"Peringatan: Rasio b/h = {ratio:.4f} berada di luar rentang "
                f"{BEAM_RATIO_MIN:.2f}–{BEAM_RATIO_MAX:.4f}."
            )
    return warnings


def slab_recap_summary(data):
    """Return title, secondary details, and optional warning for slab recap."""
    selected = float(data["Pilihan (mm)"])
    minimum = float(data["h_min_mm"])
    title = (
        f"{data['Kode panel']} · {data.get('Jenis pelat', data.get('Sistem', 'Pelat'))} · "
        f"{_mm(selected)} mm pilihan"
    )
    secondary = f"Rekomendasi minimum {minimum:.2f} mm · Pilihan {_mm(selected)} mm."
    warning = None
    if selected < minimum:
        warning = (
            f"Peringatan: Pilihan {_mm(selected)} mm < rekomendasi minimum "
            f"{minimum:.2f} mm."
        )
    return title, secondary, warning


def column_recap_summary(data):
    """Return selected-dimension title and recommendation/slenderness details."""
    selection = data.get("Pilihan pengguna (mm)")
    selection_label = (
        f"{_mm(selection)} × {_mm(selection)} mm" if selection else "Belum dipilih"
    )
    title = f"{data['Kode kolom']} · {selection_label}"
    secondary = (
        f"lu {float(data['lu (mm)']):,.0f} mm · "
        f"Balok {float(data['Lebar balok terbesar (mm)']):,.0f} mm · "
        f"Rekomendasi VECTRION {data['Rekomendasi VECTRION']} · "
        f"klu/r {float(data['Rasio kelangsingan']):.2f}"
    )
    return title, secondary


def etabs_beam_recap_key(data):
    """Use the visible DesignSect/story pair as a stable recap identity."""
    return f"{data['DesignSect']}|{data['Story']}"


def save_etabs_beam_recap(state, data):
    """Save one beam check to both the Pasca-ETABS and global analysis recaps."""
    key = etabs_beam_recap_key(data)
    saved = dict(data)
    state.setdefault("rekap_etabs_balok", {})[key] = saved.copy()
    state.setdefault("rekap_analisis_etabs", {})[key] = saved.copy()
    return key


def clear_etabs_beam_recap(state, key):
    """Clear a saved ETABS beam row from both recap views."""
    state.setdefault("rekap_etabs_balok", {}).pop(key, None)
    state.setdefault("rekap_analisis_etabs", {}).pop(key, None)
