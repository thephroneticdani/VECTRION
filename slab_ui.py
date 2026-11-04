"""Simplified Streamlit interface for preliminary slab thickness checks."""

from slab import (
    bulatkan_ke_atas_10_mm,
    hitung_tebal_minimum_tabel,
    periksa_ketebalan_pilihan,
)
from engineering_disclaimer import render_engineering_disclaimer


def render_modul_pelat(st):
    st.markdown("### Analisis Pra-Desain Pelat")
    jenis = st.radio(
        "Pilih jenis pelat",
        ["Pelat satu arah", "Pelat dua arah (pelat rusuk)"],
        horizontal=True,
        key="slab_type_simple",
    )
    desc = (
        "Pelat satu arah: beban terutama menuju dua tumpuan yang berlawanan."
        if jenis == "Pelat satu arah"
        else "Pelat dua arah menggunakan baris pelat rusuk dari Tabel 12.1 sesuai acuan yang kamu berikan."
    )
    st.info(desc + " Pastikan jenis perilaku ini sesuai dengan sistem struktur yang akan dimodelkan di ETABS.")

    st.markdown("#### Data panel")
    kode = st.text_input("Kode / nama pelat", value="P1", key="slab_code_simple")
    c1, c2 = st.columns(2)
    bentang_pendek = c1.number_input("Bentang pendek (mm)", min_value=0, value=5000, step=100, key="slab_short_simple")
    bentang_panjang = c2.number_input("Bentang panjang (mm)", min_value=0, value=6000, step=100, key="slab_long_simple")
    if jenis == "Pelat satu arah":
        arah = st.radio("Bentang yang diperiksa", ["Bentang pendek", "Bentang panjang"], horizontal=True, key="slab_direction_simple")
        bentang = bentang_pendek if arah == "Bentang pendek" else bentang_panjang
    else:
        arah = "Bentang pendek (L acuan)"
        bentang = bentang_pendek
        st.caption("Untuk pilihan dua arah, L pada tabel diambil dari bentang pendek panel sebagai asumsi awal. Pastikan asumsi ini sesuai acuan desain yang kamu gunakan.")
    kondisi = st.selectbox(
        "Kondisi tumpuan",
        ["Tumpuan sederhana", "Satu ujung menerus", "Kedua ujung menerus", "Kantilever"],
        key="slab_support_simple",
        help="Menerus berarti pelat berlanjut melewati tumpuan menuju bentang berikutnya.",
    )
    st.caption("Menerus berarti pelat berlanjut melewati tumpuan menuju bentang berikutnya.")
    pilihan = st.number_input("Tebal pelat pilihan (mm)", min_value=0, value=150, step=10, key="slab_choice_simple")

    # Small schematic that changes with the chosen system.
    if jenis == "Pelat satu arah":
        st.markdown("""<div style="border:1px solid #8B5CF6;border-radius:10px;padding:10px;background:#160D25;text-align:center;color:#F5D0FE">▰ ━━━━━━━━━━━━━ ▰<br><small>Skema satu arah: beban menuju dua tumpuan berlawanan</small></div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style="border:1px solid #8B5CF6;border-radius:10px;padding:10px;background:#160D25;text-align:center;color:#F5D0FE">┏━━━━━━━━━━┓<br>┃ &nbsp; PANEL &nbsp; ┃<br>┗━━━━━━━━━━┛<br><small>Skema dua arah: panel ditumpu pada keempat sisi (pastikan kondisi aktual)</small></div>""", unsafe_allow_html=True)

    with st.expander("Pengaturan lanjutan"):
        st.caption("Tabel acuan tidak menggunakan fy, αfm, atau faktor koreksi material. Nilai tersebut tidak dimasukkan ke rumus ini. Untuk pelat langsung ke kolom tanpa balok, metode ini belum didukung.")
        langsung_kolom = st.checkbox("Pelat langsung ditumpu kolom tanpa balok di keempat sisi", key="slab_flat_plate")

    ready = bool(kode.strip()) and bentang_pendek > 0 and bentang_panjang >= bentang_pendek and pilihan > 0 and not langsung_kolom
    if bentang_panjang < bentang_pendek:
        st.error("Bentang panjang harus sama dengan atau lebih besar dari bentang pendek.")
    if langsung_kolom:
        st.warning("Metode pelat langsung ditumpu kolom belum didukung oleh modul ini. Perhitungan tidak dijalankan.")

    if st.button("Hitung Tebal Minimum", type="primary", disabled=not ready, key="run_slab_simple"):
        hasil = hitung_tebal_minimum_tabel(bentang, jenis, kondisi)
        rekom = bulatkan_ke_atas_10_mm(hasil["h_min_mm"])
        cek = periksa_ketebalan_pilihan(pilihan, hasil["h_min_mm"])
        draft = {
            "Kode panel": kode.strip(),
            "Jenis pelat": jenis,
            "Bentang acuan (mm)": bentang,
            "Arah bentang": arah,
            "Kondisi tumpuan": kondisi,
            "Rasio L/h": hasil["rasio_L_h"],
            "h_min_mm": hasil["h_min_mm"],
            "Rekomendasi (mm)": rekom,
            "Pilihan (mm)": pilihan,
            "Selisih (mm)": round(pilihan - hasil["h_min_mm"], 2),
            "Pemeriksaan": cek,
            "Acuan": hasil["referensi"],
            "metode": hasil["metode"],
        }
        st.session_state["draft_pelat"] = draft
    draft = st.session_state.get("draft_pelat")
    if draft:
        st.markdown("#### Hasil pemeriksaan awal")
        render_engineering_disclaimer(st)
        st.write(f"**Metode:** {draft['Jenis pelat']} · {draft['metode']}")
        st.write(f"**Rasio bentang:** L/h = {draft['Rasio L/h']:g} · **Bentang acuan:** {draft['Bentang acuan (mm)']:,} mm · **Tumpuan:** {draft['Kondisi tumpuan']}")
        x, y, z = st.columns(3)
        x.metric("h minimum teoritis", f"{draft['h_min_mm']:.2f} mm")
        y.metric("Rekomendasi praktis", f"{draft['Rekomendasi (mm)']} mm")
        z.metric("Tebal pilihan", f"{draft['Pilihan (mm)']} mm", delta=f"{draft['Selisih (mm)']:+.2f} mm dari minimum")
        (st.success if draft["Pilihan (mm)"] >= draft["h_min_mm"] else st.warning)(draft["Pemeriksaan"])
        st.caption(f"Acuan: {draft['Acuan']}. Pembulatan ke atas per 10 mm adalah aturan praktis aplikasi, bukan persyaratan tabel.")
        with st.expander("Detail perhitungan"):
            st.code(f"h_min = L / rasio\n     = {draft['Bentang acuan (mm)']} / {draft['Rasio L/h']}\n     = {draft['h_min_mm']:.2f} mm")
            st.caption("Tanpa perhitungan lendutan. Hasil ini hanya pemeriksaan awal dimensi sebelum pemodelan ETABS.")
        if st.button("Simpan / Perbarui rekap pelat", key="save_slab_simple"):
            st.session_state["rekap_pelat"][draft["Kode panel"].upper()] = draft
            st.success("Rekap pelat diperbarui.")
    st.caption("Pemeriksaan ini bukan desain struktur lengkap dan tidak menyatakan pelat aman secara struktural.")
