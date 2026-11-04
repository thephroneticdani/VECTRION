
def hitung_tinggi_minimum(bentang_mm, kondisi_tumpuan):
    """
    Menghitung tinggi minimum awal balok berdasarkan
    rasio pada SNI 2847:2019 Pasal 9.3.1.1.

    Catatan:
    Perhitungan ini merupakan pemeriksaan awal,
    bukan verifikasi keamanan struktur.
    """

    rasio_tinggi = {
        "Tumpuan sederhana": 16,
        "Menerus satu sisi": 18.5,
        "Menerus dua sisi": 21,
        "Kantilever": 8,
    }

    if bentang_mm <= 0:
        raise ValueError("Bentang harus lebih besar dari 0 mm.")

    if kondisi_tumpuan not in rasio_tinggi:
        raise ValueError("Kondisi tumpuan tidak dikenali.")

    rasio = rasio_tinggi[kondisi_tumpuan]
    tinggi_minimum = bentang_mm / rasio

    return tinggi_minimum


def bulatkan_ke_atas_50_mm(tinggi_mm):
    """Membulatkan tinggi ke atas ke kelipatan 50 mm."""

    if tinggi_mm <= 0:
        raise ValueError("Tinggi harus lebih besar dari 0 mm.")

    return int((tinggi_mm + 49) // 50 * 50)

def buat_alternatif_lebar(tinggi_mm):
    """
    Membuat dua alternatif lebar awal balok:
    0,5h dan 2/3h.

    Rasio ini merupakan pendekatan aplikasi,
    bukan ketentuan dimensi wajib dari SNI.
    """

    if tinggi_mm <= 0:
        raise ValueError("Tinggi harus lebih besar dari 0 mm.")

    alternatif = [
        {
            "Alternatif": "A",
            "Rasio b/h": "1/2",
            "Lebar (mm)": int(tinggi_mm * 0.5),
        },
        {
            "Alternatif": "B",
            "Rasio b/h": "2/3",
            "Lebar (mm)": int(-(-tinggi_mm * 2 // 3)),
        },
    ]

    for item in alternatif:
        item["Tinggi (mm)"] = tinggi_mm
        item["Luas penampang (mm²)"] = (
            item["Lebar (mm)"] * tinggi_mm
        )

    return alternatif

def hitung_lebar_manual(tinggi_mm, rasio_b_h):
    """
    Menghitung lebar dan luas penampang berdasarkan
    rasio b/h yang dipilih pengguna.

    Batas rasio 0,5 sampai 2/3 merupakan aturan
    aplikasi, bukan persyaratan dimensi wajib SNI.
    """

    if tinggi_mm <= 0:
        raise ValueError("Tinggi harus lebih besar dari 0 mm.")

    if not 0.5 <= rasio_b_h <= (2 / 3):
        raise ValueError(
            "Rasio b/h harus antara 0,5 dan 0,667."
        )

    lebar_mm = int(-(-(tinggi_mm * rasio_b_h) // 1))
    luas_mm2 = lebar_mm * tinggi_mm

    return {
        "Rasio b/h": rasio_b_h,
        "Lebar (mm)": lebar_mm,
        "Tinggi (mm)": tinggi_mm,
        "Luas penampang (mm²)": luas_mm2,
    }
