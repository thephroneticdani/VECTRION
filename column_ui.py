"""Streamlit presentation layer for preliminary column sizing."""

from column import (
    calculate_square_column_slenderness,
    convert_unbraced_height_to_mm,
    recommend_square_column,
    validate_column_code,
)


def render_column_module(st):
    st.markdown("### Analisis Pra-Desain Kolom")
    st.caption("Penentuan geometri awal kolom beton bertulang sebelum pemodelan ETABS / SAP2000.")
    st.info("Modul ini memberi ukuran awal dan informasi kelangsingan. Ini bukan desain lengkap dan tidak menyatakan kolom aman.")

    st.markdown("#### Data kolom")
    code = st.text_input("Kode kolom", value="K1", key="column_code")
    left, right = st.columns(2)
    with left:
        lu_value = st.number_input("Tinggi kolom tak tertumpu, lu", min_value=0.0, value=3.0, step=0.1, key="column_lu")
        lu_unit = st.selectbox("Satuan lu", ["m", "mm"], key="column_lu_unit")
    with right:
        beam_width = st.number_input("Lebar balok terbesar yang bertemu kolom (mm)", min_value=0.0, value=250.0, step=25.0, key="column_beam_width")
        st.caption("lu adalah tinggi segmen kolom yang tidak tertumpu, bukan otomatis tinggi total gedung.")

    st.markdown("#### Dimensi pilihan pengguna (opsional)")
    use_selected = st.checkbox("Simpan dimensi kolom pilihan saya", key="column_use_selection")
    selected_side = st.number_input(
        "Sisi kolom persegi pilihan (mm)", min_value=1, value=300, step=50,
        key="column_selected_side", disabled=not use_selected,
        help="Pilihan ini disimpan terpisah dan tidak diubah otomatis ketika rekomendasi berubah.",
    )

    if st.button("Hitung rekomendasi awal", type="primary", key="run_column"):
        try:
            code_value = validate_column_code(code)
            lu_mm = convert_unbraced_height_to_mm(lu_value, lu_unit)
            recommendation = recommend_square_column(beam_width)
            selected = float(selected_side) if use_selected else None
            if selected is not None and selected <= 0:
                raise ValueError("Dimensi pilihan harus lebih besar dari 0 mm.")
            sizing_side = selected if selected is not None else recommendation["width_mm"]
            slenderness = calculate_square_column_slenderness(lu_mm, sizing_side, k=1.0)
            st.session_state["draft_kolom"] = {
                "Kode kolom": code_value,
                "lu (mm)": lu_mm,
                "Lebar balok terbesar (mm)": float(beam_width),
                "Rekomendasi VECTRION": recommendation["section"],
                "Sisi rekomendasi (mm)": recommendation["width_mm"],
                "Pilihan pengguna (mm)": selected,
                "Dimensi untuk kelangsingan (mm)": sizing_side,
                "k": slenderness["k"],
                "r (mm)": slenderness["radius_gyration_mm"],
                "Rasio kelangsingan": slenderness["slenderness_ratio"],
            }
            st.session_state.pop("column_error", None)
        except ValueError as exc:
            st.session_state["column_error"] = str(exc)
    if st.session_state.get("column_error"):
        st.error(st.session_state["column_error"])

    draft = st.session_state.get("draft_kolom")
    if draft:
        st.markdown("#### Informasi kolom")
        st.write(f"**{draft['Kode kolom']}** · lu {draft['lu (mm)']:,.0f} mm · lebar balok terbesar {draft['Lebar balok terbesar (mm)']:,.0f} mm")
        a, b = st.columns(2)
        a.metric("Rekomendasi otomatis", draft["Rekomendasi VECTRION"])
        b.metric("Dimensi pilihan pengguna", f"{draft['Pilihan pengguna (mm)']:,.0f} × {draft['Pilihan pengguna (mm)']:,.0f} mm" if draft["Pilihan pengguna (mm)"] else "Belum dipilih")
        st.markdown("#### Informasi kelangsingan awal")
        c1, c2, c3 = st.columns(3)
        c1.metric("Asumsi k", f"{draft['k']:.1f}")
        c2.metric("Radius girasi, r = 0,3h", f"{draft['r (mm)']:,.1f} mm")
        c3.metric("Rasio klu/r", f"{draft['Rasio kelangsingan']:.2f}")
        st.caption(f"Perhitungan menggunakan sisi {draft['Dimensi untuk kelangsingan (mm)']:,.0f} mm dan lu {draft['lu (mm)']:,.0f} mm. k = 1,0 hanya asumsi awal, bukan faktor universal.")
        st.warning("Nilai klu/r ditampilkan sebagai informasi awal saja. Klasifikasi goyangan, rasio momen ujung, dan faktor k aktual belum dievaluasi; efek kelangsingan harus diperiksa dalam analisis struktur.")
        st.markdown("#### Catatan teknis")
        st.markdown(
            "- **Rekomendasi VECTRION** memakai heuristik aplikasi: `b_col = max(300 mm, lebar balok terbesar)`, menghasilkan penampang persegi. Ini bukan rumus dimensi yang ditetapkan SNI.\n"
            "- Jika kolom merupakan bagian **SRPMK**, SNI 2847:2019 Pasal 18.7.2.1 menetapkan dimensi terkecil, diukur melalui pusat geometri, ≥ 300 mm dan rasio dimensi terkecil terhadap sisi tegak lurusnya ≥ 0,4. Ketentuan ini tidak digeneralisasi ke semua sistem kolom.\n"
            "- Pasal 6.2.5 memberi kondisi untuk mengabaikan pengaruh kelangsingan pada keadaan yang berlaku: kolom yang tidak ditahan terhadap goyangan samping `klu/r ≤ 22`; kolom yang ditahan terhadap goyangan `klu/r ≤ 34 + 12(M1/M2)` dan `klu/r ≤ 40`. Dalam SNI 2019, M1/M2 negatif untuk kurvatur tunggal dan positif untuk kurvatur ganda. Modul ini tidak memiliki data klasifikasi rangka dan momen ujung, sehingga tidak memberi status lulus/gagal.\n"
            "- Pasal 18.7.3.2 mensyaratkan `ΣMnc ≥ 1,2ΣMnb` untuk pemeriksaan strong-column–weak-beam. Perlu kapasitas momen kolom dan balok pada joint; pemeriksaan ini tidak dilakukan di sini."
        )
        st.caption("Referensi: [Teks SNI 2847:2019](https://lmsspada.kemdiktisaintek.go.id/pluginfile.php/543340/mod_resource/content/1/SNI%202847-2019%20Persyaratan%20Beton%20Struktural%20Untuk%20Bangunan%20Gedung%20dan%20penjelasan.pdf) · [Katalog standar BSN](https://pesta.bsn.go.id/produk/detail/12731-sni28472019)")
        if st.button("Simpan / perbarui rekap kolom", key="save_column"):
            st.session_state["rekap_kolom"][draft["Kode kolom"].upper()] = dict(draft)
            st.success(f"Rekap {draft['Kode kolom']} tersimpan.")
