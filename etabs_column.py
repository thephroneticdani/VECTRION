"""Basic column longitudinal-steel area checks; not a strength design module."""

from math import isfinite, pi


BAR_DIAMETERS_MM = (8, 10, 12, 13, 16, 19, 22, 25, 29, 32)


def hitung_tulangan_kolom(width_mm, depth_mm, min_ratio_percent, diameters, quantities):
    """Check supplied longitudinal bar area against user-selected 1–8% gross area."""
    try:
        width, depth, ratio = map(float, (width_mm, depth_mm, min_ratio_percent))
        ds = [float(value) for value in diameters]
        ns = [float(value) for value in quantities]
    except (TypeError, ValueError) as exc:
        raise ValueError("Dimensi, rasio, diameter, dan jumlah harus berupa angka.") from exc
    if not all(isfinite(value) for value in (width, depth, ratio, *ds, *ns)):
        raise ValueError("Semua input harus berupa angka terbatas.")
    if width <= 0 or depth <= 0:
        raise ValueError("Lebar dan tinggi kolom harus lebih besar dari 0 mm.")
    if not 1 <= ratio <= 8:
        raise ValueError("Target rasio tulangan minimum harus antara 1% dan 8%.")
    if len(ds) != 3 or len(ns) != 3:
        raise ValueError("Kolom memerlukan tepat tiga pasangan diameter dan jumlah.")
    if any(d <= 0 for d in ds):
        raise ValueError("Diameter tulangan harus lebih besar dari 0 mm.")
    if any(n < 0 or not n.is_integer() for n in ns):
        raise ValueError("Jumlah batang harus bilangan bulat nol atau lebih.")

    gross_area = width * depth
    provided = sum(pi * diameter**2 / 4 * int(quantity) for diameter, quantity in zip(ds, ns))
    required = gross_area * ratio / 100
    maximum = gross_area * 0.08
    actual_ratio = provided / gross_area * 100
    if provided < required:
        status = "Kurang dari minimum"
    elif provided > maximum:
        status = "Melebihi 8%"
    else:
        status = "Memenuhi"
    return {
        "Luas penampang (mm²)": gross_area,
        "Rasio minimum (%)": ratio,
        "As minimum (mm²)": required,
        "As maksimum 8% (mm²)": maximum,
        "As tersedia (mm²)": provided,
        "Rasio aktual (%)": actual_ratio,
        "Status": status,
    }


def format_kombinasi_tulangan_kolom(diameters, quantities):
    groups = [
        f"{int(float(quantity))}D{int(float(diameter))}"
        for diameter, quantity in zip(diameters, quantities)
        if int(float(quantity or 0)) > 0
    ]
    return " + ".join(groups) if groups else "—"
