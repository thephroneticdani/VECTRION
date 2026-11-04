"""Pure calculation functions for preliminary slab thickness checks.

Equations implemented from SNI 2847:2019 sections 7.3.1.1 and 8.3.1.1–8.3.1.2.
This module deliberately does not perform strength or deflection design.
"""


def _positive(value, name):
    if value <= 0:
        raise ValueError(f"{name} harus lebih besar dari 0.")


def bulatkan_ke_atas_10_mm(tebal_mm):
    """Round a positive thickness up to the next 10 mm increment."""
    _positive(tebal_mm, "Ketebalan")
    return int(-(-tebal_mm // 10) * 10)


def hitung_pelat_satu_arah(bentang, kondisi, fy=420, wc=2300):
    """Minimum nonprestressed solid one-way slab thickness, SNI 7.3.1.1.

    ``wc`` is concrete density in kg/m3. Normal-weight concrete is represented
    by 2300; lightweight concrete is supported only in the SNI range 1440–1840.
    """
    _positive(bentang, "Bentang")
    _positive(fy, "fy")
    _positive(wc, "Berat isi beton")
    denominator = {
        "Tumpuan sederhana": 20,
        "Satu ujung menerus": 24,
        "Kedua ujung menerus": 28,
        "Kantilever": 10,
    }
    if kondisi not in denominator:
        raise ValueError("Kondisi tumpuan pelat tidak dikenali.")
    if not (wc == 2300 or 1440 <= wc <= 1840):
        raise ValueError("Berat isi beton yang didukung: 2300 kg/m³ (normal) atau 1440–1840 kg/m³ (ringan).")
    factor_fy = 0.4 + fy / 700 if fy > 420 else 1.0
    factor_weight = max(1.65 - 0.0003 * wc, 1.09) if wc != 2300 else 1.0
    h_min = bentang / denominator[kondisi] * factor_fy * factor_weight
    return {
        "h_min_mm": h_min,
        "fy_factor": factor_fy,
        "weight_factor": factor_weight,
        "metode": "SNI 2847:2019 Pasal 7.3.1.1, Tabel 7.3.1.1; beton ringan sesuai 7.3.1.1.2 bila dipilih.",
    }


def _interpolasi_fy(fy, values):
    if fy < 280 or fy > 520:
        raise ValueError("Untuk metode Tabel 8.3.1.1, fy harus berada pada rentang 280–520 MPa.")
    if fy <= 420:
        lo, hi = 280, 420
    else:
        lo, hi = 420, 520
    return values[lo] + (values[hi] - values[lo]) * (fy - lo) / (hi - lo)


def _ketebalan_8311(ln, fy, panel, drop, edge_alpha):
    if panel not in ("Interior", "Eksterior"):
        raise ValueError("Kategori panel tidak dikenali.")
    without_drop = {
        "Interior": {280: 36, 420: 33, 520: 31},
        "Eksterior": {280: 36 if edge_alpha >= .8 else 33, 420: 33 if edge_alpha >= .8 else 30, 520: 31 if edge_alpha >= .8 else 28},
    }
    with_drop = {
        "Interior": {280: 40, 420: 36, 520: 34},
        "Eksterior": {280: 40 if edge_alpha >= .8 else 36, 420: 36 if edge_alpha >= .8 else 33, 520: 34 if edge_alpha >= .8 else 31},
    }
    divisors = _interpolasi_fy(fy, with_drop[panel] if drop else without_drop[panel])
    return max(ln / divisors, 100 if drop else 125), divisors


def hitung_pelat_dua_arah(short, long, fy=420, alphas=None, panel="Interior", drop=False, edge_cont="Menerus", edge_alpha=None, tanpa_balok_interior=False):
    """Minimum two-way slab thickness for supported panel conditions.

    Four beam stiffness ratios (alpha_f) are needed to calculate alpha_fm.
    For alpha_fm <= 0.2, the referenced SNI 8.3.1.1 table is applied only
    to panels with no interior beams and aspect ratio <= 2.
    """
    _positive(short, "Bentang pendek")
    _positive(long, "Bentang panjang")
    _positive(fy, "fy")
    if long < short:
        raise ValueError("Bentang panjang harus lebih besar atau sama dengan bentang pendek.")
    beta = long / short
    if beta > 2:
        raise ValueError("Rasio bentang panjang/pendek > 2 harus diperiksa sebagai pelat satu arah menurut SNI 8.3.1.2.")
    if not alphas or len(alphas) != 4:
        raise ValueError("Masukkan rasio kekakuan αf untuk keempat sisi balok.")
    if any(a < 0 for a in alphas):
        raise ValueError("Rasio kekakuan αf tidak boleh negatif.")
    alpha_fm = sum(alphas) / 4
    edge_alpha = min(alphas) if edge_alpha is None else edge_alpha
    if edge_alpha < 0:
        raise ValueError("Rasio kekakuan balok tepi tidak boleh negatif.")
    if edge_cont not in ("Menerus", "Tidak menerus"):
        raise ValueError("Kondisi tepi panel tidak dikenali.")
    if alpha_fm <= .2:
        if not tanpa_balok_interior:
            raise ValueError("Untuk αfm ≤ 0,2, Pasal 8.3.1.2 merujuk 8.3.1.1 yang hanya didukung untuk panel tanpa balok interior. Konfirmasi kondisi tersebut untuk melanjutkan.")
        hmin, divisor = _ketebalan_8311(long, fy, panel, drop, edge_alpha)
        method = ("SNI 2847:2019 Pasal 8.3.1.2 merujuk Pasal 8.3.1.1; "
                  f"Tabel 8.3.1.1 (fy interpolasi, pembagi {divisor:.3f}, "
                  f"minimum {'100' if drop else '125'} mm).")
    elif alpha_fm <= 2:
        hmin = max(long * (0.8 + fy / 1400) / (36 + 5 * beta * (alpha_fm - .2)), 125)
        method = "SNI 2847:2019 Pasal 8.3.1.2, Tabel 8.3.1.2(b),(c)."
    else:
        hmin = max(long * (0.8 + fy / 1400) / (36 + 9 * beta), 90)
        method = "SNI 2847:2019 Pasal 8.3.1.2, Tabel 8.3.1.2(d),(e)."
    edge_adjustment = False
    if edge_cont == "Tidak menerus" and panel == "Eksterior":
        if edge_alpha >= .8:
            method += " Balok tepi tidak menerus memenuhi αf ≥ 0,80 (8.3.1.2.1)."
        else:
            if alpha_fm <= .2:
                raise ValueError("Panel eksterior αfm ≤ 0,2 dengan tepi tidak menerus dan αf < 0,8 tidak didukung; pasal 8.3.1.2.1 mensyaratkan minimum (b)/(d) +10%.")
            hmin *= 1.10
            edge_adjustment = True
            method += " Tebal dinaikkan 10% untuk tepi eksterior tidak menerus (8.3.1.2.1)."
    return {
        "h_min_mm": hmin,
        "beta": beta,
        "alpha_fm": alpha_fm,
        "edge_adjustment": edge_adjustment,
        "metode": method,
    }


RASIO_TABEL_12_1 = {
    "Pelat satu arah": {
        "Tumpuan sederhana": 20,
        "Satu ujung menerus": 24,
        "Kedua ujung menerus": 28,
        "Kantilever": 10,
    },
    "Pelat dua arah (pelat rusuk)": {
        "Tumpuan sederhana": 16,
        "Satu ujung menerus": 18.5,
        "Kedua ujung menerus": 21,
        "Kantilever": 8,
    },
}


def hitung_tebal_minimum_tabel(bentang_mm, jenis_pelat, kondisi_tumpuan):
    """Calculate h_min = L / ratio from the user's supplied Tabel 12.1 image."""
    _positive(bentang_mm, "Bentang")
    if jenis_pelat not in RASIO_TABEL_12_1:
        raise ValueError("Jenis pelat belum didukung oleh tabel acuan.")
    if kondisi_tumpuan not in RASIO_TABEL_12_1[jenis_pelat]:
        raise ValueError("Kondisi tumpuan tidak dikenali.")
    rasio = RASIO_TABEL_12_1[jenis_pelat][kondisi_tumpuan]
    return {
        "bentang_mm": bentang_mm,
        "jenis_pelat": jenis_pelat,
        "kondisi_tumpuan": kondisi_tumpuan,
        "rasio_L_h": rasio,
        "h_min_mm": bentang_mm / rasio,
        "metode": f"h_min = L/{rasio:g}",
        "referensi": "Tabel 12.1 Tebal Minimum Pelat (gambar acuan dari pengguna)",
    }


def periksa_ketebalan_pilihan(pilihan, minimum):
    """Return a concise result for a proposed thickness."""
    _positive(pilihan, "Ketebalan pilihan")
    _positive(minimum, "Ketebalan minimum")
    if pilihan < minimum:
        return f"Tidak memenuhi pemeriksaan awal: {pilihan:g} mm < {minimum:.2f} mm."
    return f"Memenuhi batas ketebalan minimum awal: {pilihan:g} mm ≥ {minimum:.2f} mm."
