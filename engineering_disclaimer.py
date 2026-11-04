"""Standard engineering disclaimer shared across VECTRION pages."""

ENGINEERING_DISCLAIMER = (
    "PERHATIAN — VECTRION merupakan alat bantu pra-desain untuk estimasi dan "
    "pemeriksaan awal dimensi elemen struktur. Seluruh hasil perhitungan dan "
    "rekomendasi dimensi wajib melalui analisis struktur, verifikasi kapasitas, "
    "stabilitas, serta pemeriksaan engineering sesuai standar yang berlaku "
    "sebelum digunakan dalam desain final. Output aplikasi ini tidak boleh "
    "digunakan secara langsung sebagai dasar pelaksanaan konstruksi."
)


def render_engineering_disclaimer(st) -> None:
    """Show the required preliminary-design warning in a visible callout."""
    st.warning(ENGINEERING_DISCLAIMER, icon="⚠️")
