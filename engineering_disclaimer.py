"""Standard engineering disclaimer shared across VECTRION pages."""

ENGINEERING_DISCLAIMER = (
    "PERHATIAN — Hasil VECTRION adalah estimasi awal untuk pra-desain, bukan "
    "desain final. Verifikasi melalui analisis struktur dan pemeriksaan "
    "insinyur sebelum digunakan untuk konstruksi."
)


def render_engineering_disclaimer(st) -> None:
    """Show the required preliminary-design warning in a visible callout."""
    st.warning(ENGINEERING_DISCLAIMER, icon="⚠️")
