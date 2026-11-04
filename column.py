"""Pure helpers for preliminary reinforced-concrete column sizing.

The automatic size rule is a VECTRION application heuristic, not an SNI equation.
This module does not design reinforcement or verify column strength/stability.
"""

import math


def _positive_finite(value, label):
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} harus berupa angka yang valid.") from exc
    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{label} harus lebih besar dari 0.")
    return number


def convert_unbraced_height_to_mm(height, unit):
    """Convert the actual unbraced segment height (lu) to millimeters."""
    value = _positive_finite(height, "Tinggi tak tertumpu (lu)")
    if unit == "m":
        value *= 1000
    elif unit != "mm":
        raise ValueError("Satuan lu harus m atau mm.")
    return value


def recommend_square_column(largest_beam_width_mm):
    """Return b_col=max(300 mm, largest intersecting beam width), rounded up to 1 mm."""
    beam_width = _positive_finite(largest_beam_width_mm, "Lebar balok terbesar")
    side = int(math.ceil(max(300.0, beam_width)))
    return {"width_mm": side, "depth_mm": side, "section": f"{side} × {side} mm"}


def calculate_square_column_slenderness(lu_mm, side_mm, k=1.0):
    """Calculate preliminary lambda=k*lu/(0.3h) for a square section."""
    lu = _positive_finite(lu_mm, "Tinggi tak tertumpu (lu)")
    side = _positive_finite(side_mm, "Sisi kolom")
    effective_length_factor = _positive_finite(k, "Faktor panjang efektif k")
    radius = 0.3 * side
    return {
        "k": effective_length_factor,
        "lu_mm": lu,
        "side_mm": side,
        "radius_gyration_mm": radius,
        "slenderness_ratio": effective_length_factor * lu / radius,
    }


def validate_column_code(code):
    if not isinstance(code, str) or not code.strip():
        raise ValueError("Kode kolom tidak boleh kosong.")
    return code.strip()
