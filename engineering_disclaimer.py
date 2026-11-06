"""Standard engineering disclaimer shared across VECTRION pages."""

ENGINEERING_DISCLAIMER = (
    "PERHATIAN — Hasil VECTRION adalah estimasi awal, bukan desain final. "
    "Verifikasi dengan analisis struktur dan insinyur sebelum digunakan."
)


def render_engineering_disclaimer(st, message=None) -> None:
    """Show the required preliminary-design warning in a visible callout."""
    st.warning(message or ENGINEERING_DISCLAIMER, icon="⚠️")
