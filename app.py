import streamlit as st
from pathlib import Path
import base64
from beam import (
    hitung_tinggi_minimum,
    bulatkan_ke_atas_50_mm,
    buat_alternatif_lebar,
    hitung_lebar_manual,
)

st.set_page_config(
    page_title="VECTRION — Structural Engineering Suite",
    page_icon="🏗️",
    layout="wide",
)

from styling import inject_global_styles
from column_ui import render_column_module
from recap import clear_etabs_beam_recap, clear_etabs_column_recap
from recap_table_ui import render_recap_table
from recap_export import build_recap_html
from etabs_beam import format_kombinasi_tulangan, status_kombinasi_balok
from engineering_disclaimer import render_engineering_disclaimer
from post_etabs_ui import render_post_etabs_beam, render_post_etabs_column

# ==================================================
# NAVIGASI DAN SESSION STATE
# ==================================================
from slab import (
    hitung_pelat_satu_arah,
    hitung_pelat_dua_arah,
    bulatkan_ke_atas_10_mm,
    periksa_ketebalan_pilihan,
)
from navigation import initialize_state, navigate
from slab_ui import render_modul_pelat

initialize_state(st.session_state)
st.session_state.setdefault("rekap_kolom", {})
st.session_state.setdefault("navigation_hidden", False)
st.session_state.setdefault("theme_mode", "Terang")
inject_global_styles(st, navigation_hidden=st.session_state["navigation_hidden"], theme=st.session_state["theme_mode"])

def pindah(halaman):
    navigate(st.session_state, halaman)

def toggle_navigation():
    st.session_state["navigation_hidden"] = not st.session_state["navigation_hidden"]

def toggle_theme():
    st.session_state["theme_mode"] = "Gelap" if st.session_state["theme_mode"] == "Terang" else "Terang"

logo_path = Path(__file__).parent / "assets" / "vectrion_logo_jawa.svg"
logo_data = base64.b64encode(logo_path.read_bytes()).decode("ascii") if logo_path.exists() else None

with st.sidebar:
    if logo_data:
        st.markdown(
            f'<div class="brand-logo brand-logo-sidebar"><img src="data:image/svg+xml;base64,{logo_data}" alt="VECTRION — Structural Engineering Suite"></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown("## VECTRION")
    st.caption("Structural Engineering Suite")
    st.markdown("---")
    with st.container(key="primary-navigation"):
        st.caption("Navigasi aplikasi")
        page_buttons = (("Beranda", "⌂"), ("Pra-Desain", "▤"), ("Pasca-ETABS", "⌁"))
        for page, icon in page_buttons:
            active = st.session_state["halaman"] == page or (
                page == "Pasca-ETABS" and st.session_state["halaman"].startswith("Pasca-ETABS-")
            )
            st.button(
                f"{icon}  {page}",
                key=f"nav_{page}",
                type="primary" if active else "secondary",
                use_container_width=True,
                on_click=pindah,
                args=(page,),
            )
        st.button(
            f"☾  Gelap" if st.session_state["theme_mode"] == "Terang" else "☀  Terang",
            key="toggle_theme", type="secondary", use_container_width=True,
            on_click=toggle_theme,
        )
    if st.session_state["halaman"] == "Pra-Desain":
        st.radio("Modul pra-desain", ["Balok", "Pelat", "Kolom"], horizontal=False, key="modul_pra")
    if st.session_state["halaman"].startswith("Pasca-ETABS-"):
        st.caption("Modul Pasca-ETABS")
        with st.container(key="post-etabs-module-navigation"):
            beam_nav, column_nav = st.columns(2, gap="small")
            with beam_nav:
                st.button(
                    "▤  Balok", key="nav_Pasca-ETABS-Balok",
                    type="primary" if st.session_state["halaman"] == "Pasca-ETABS-Balok" else "secondary",
                    use_container_width=True, on_click=pindah, args=("Pasca-ETABS-Balok",),
                )
            with column_nav:
                st.button(
                    "▥  Kolom", key="nav_Pasca-ETABS-Kolom",
                    type="primary" if st.session_state["halaman"] == "Pasca-ETABS-Kolom" else "secondary",
                    use_container_width=True, on_click=pindah, args=("Pasca-ETABS-Kolom",),
                )

menu_col, title_col = st.columns([0.12, 0.88], vertical_alignment="center")
with menu_col:
    with st.container(key="navigation-toggle"):
        st.button("☰", key="toggle_navigation", type="primary", help="Sembunyikan / tampilkan panel navigasi", on_click=toggle_navigation)
with title_col:
    st.title("VECTRION")
    st.caption("Structural Engineering Suite · Pemeriksaan dimensi awal struktur beton bertulang")

if st.session_state["halaman"] == "Beranda":
    render_engineering_disclaimer(st)
    with st.container(key="home-hero"):
        st.html(
            """<div class="vx-home-video-layer" aria-hidden="true">
<video autoplay muted loop playsinline preload="metadata" tabindex="-1">
<source src="/app/static/hero_construction.mp4" type="video/mp4">
</video><div class="vx-home-video-shade"></div></div>"""
        )
        hero_copy, hero_brand = st.columns([1.15, 0.85], vertical_alignment="center")
        with hero_copy:
            st.markdown("## Rekayasa struktur, dimulai dari pradesain")
            st.write("Pilih alur analisis untuk memulai pemeriksaan dimensi awal.")
            st.caption("Pra-desain elemen beton bertulang dalam satu ruang kerja.")
        with hero_brand:
            if logo_data:
                st.markdown(
                    f'<div class="brand-logo brand-logo-hero"><img src="data:image/svg+xml;base64,{logo_data}" alt="VECTRION — Structural Engineering Suite"></div>',
                    unsafe_allow_html=True,
                )
    kiri, kanan = st.columns(2)
    with kiri:
        with st.container(border=True):
            st.markdown("### Analisis Pra-Desain")
            st.write("Pemeriksaan awal dimensi balok dan pelat.")
            st.button("Buka Pra-Desain →", type="primary", use_container_width=True,
                      on_click=pindah, args=("Pra-Desain",))
    with kanan:
        with st.container(border=True):
            st.markdown("### Analisis Pasca-ETABS")
            st.write("Alur pemeriksaan hasil analisis struktur.")
            st.button("Buka Pasca-ETABS →", use_container_width=True,
                      on_click=pindah, args=("Pasca-ETABS",))

elif st.session_state["halaman"] == "Pra-Desain":
    render_engineering_disclaimer(st)
    st.markdown("## Analisis Pra-Desain")
    modul = st.session_state["modul_pra"]
    if modul == "Kolom":
        render_column_module(st)
    elif modul == "Balok":
        st.markdown("### Data balok")
        with st.form("form_data_balok"):
            kode = st.text_input("Kode balok", value="B1")
            bentang = st.number_input("Panjang bentang (mm)", min_value=1, value=6000, step=100)
            kondisi = st.selectbox("Kondisi tumpuan", ["Tumpuan sederhana", "Menerus satu sisi", "Menerus dua sisi", "Kantilever"])
            hitung_awal = st.form_submit_button("Hitung tinggi minimum", type="primary")
        if hitung_awal:
            if not kode.strip():
                st.error("Kode balok tidak boleh kosong.")
            else:
                hmin = hitung_tinggi_minimum(bentang, kondisi)
                st.session_state["draft_balok"] = {"kode": kode.strip(), "bentang": bentang, "kondisi": kondisi, "h_min": hmin, "h_rekom": bulatkan_ke_atas_50_mm(hmin)}
                st.session_state.pop("tinggi_pilihan_input", None)
                st.session_state.pop("lebar_pilihan_input", None)
        draft = st.session_state["draft_balok"]
        if draft:
            st.write(f"**{draft['kode']}** · Bentang {draft['bentang']} mm · {draft['kondisi']}")
            c1, c2 = st.columns(2)
            c1.metric("Tinggi minimum awal", f"{draft['h_min']:.2f} mm")
            c2.metric("Rekomendasi praktis", f"{draft['h_rekom']} mm")
            st.caption("Pembulatan ke atas per 50 mm adalah aturan praktis aplikasi.")
            with st.form("form_dimensi_final"):
                tinggi = st.number_input("Tinggi balok pilihan (mm)", min_value=1, value=int(draft["h_rekom"]), step=50, key="tinggi_pilihan_input")
                lebar = st.number_input("Lebar balok pilihan (mm)", min_value=1, value=max(1, int(draft["h_rekom"] * .5)), step=25, key="lebar_pilihan_input")
                simpan = st.form_submit_button("Simpan / Perbarui hasil")
            st.markdown("#### Alternatif lebar otomatis")
            st.table(buat_alternatif_lebar(tinggi))
            rasio, luas = lebar / tinggi, lebar * tinggi
            c1, c2, c3 = st.columns(3)
            c1.metric("Rasio b/h", f"{rasio:.3f}")
            c2.metric("Luas penampang", f"{luas:,} mm²")
            c3.metric("Dimensi b × h", f"{lebar} × {tinggi} mm")
            if tinggi < draft["h_min"]:
                st.warning("Tinggi pilihan berada di bawah tinggi minimum awal.")
            elif tinggi < draft["h_rekom"]:
                st.info("Pilihan di bawah rekomendasi praktis, tetapi tidak di bawah tinggi minimum awal.")
            else:
                st.success("Pilihan memenuhi tinggi minimum awal berdasarkan rasio aplikasi.")
            if not .5 <= rasio <= 2 / 3:
                st.warning("Rasio b/h berada di luar rentang pendekatan aplikasi 0,5–0,667.")
            if simpan:
                k = draft["kode"].upper()
                st.session_state["rekap_balok"][k] = {"Kode balok": draft["kode"], "Bentang (mm)": draft["bentang"], "Kondisi tumpuan": draft["kondisi"], "Tinggi minimum (mm)": round(draft["h_min"], 2), "Tinggi rekomendasi (mm)": draft["h_rekom"], "Lebar pilihan (mm)": int(lebar), "Tinggi pilihan (mm)": int(tinggi), "Dimensi (b × h)": f"{int(lebar)} × {int(tinggi)} mm", "Rasio b/h": round(rasio, 3), "Luas penampang (mm²)": int(luas)}
                st.success(f"Hasil {draft['kode']} tersimpan.")
    else:
        render_modul_pelat(st)
elif st.session_state["halaman"] == "Pasca-ETABS":
    st.markdown("## Analisis Pasca-ETABS")
    render_engineering_disclaimer(st)
    st.write("Pilih elemen yang ingin diperiksa dari hasil ekspor ETABS.")
    beam_col, column_col = st.columns(2)
    with beam_col, st.container(border=True):
        st.markdown("### Balok")
        st.write("Unggah ringkasan desain dan bandingkan kebutuhan As dengan tulangan pilihan.")
        st.button("Buka Pasca-ETABS Balok →", type="primary", use_container_width=True,
                  on_click=pindah, args=("Pasca-ETABS-Balok",))
    with column_col, st.container(border=True):
        st.markdown("### Kolom")
        st.write("Periksa rasio luas tulangan longitudinal kolom dengan tiga kombinasi diameter dan jumlah batang.")
        st.button("Buka Pasca-ETABS Kolom →", use_container_width=True,
                  on_click=pindah, args=("Pasca-ETABS-Kolom",))
elif st.session_state["halaman"] == "Pasca-ETABS-Balok":
    render_post_etabs_beam(st)
elif st.session_state["halaman"] == "Pasca-ETABS-Kolom":
    render_engineering_disclaimer(st)
    render_post_etabs_column(st)

# Rekap lintas halaman: tetap berada di session_state saat navigasi.
with st.container(key="recap-section"):
    st.divider()
    st.markdown("### Rekap analisis")
    st.download_button(
        "⬇️ Unduh rekap siap cetak",
        data=build_recap_html(st.session_state),
        file_name="rekap-analisis-vectrion.html",
        mime="text/html",
        key="download-recap",
        help="Unduh halaman rekap; buka file lalu pilih Cetak / Simpan PDF.",
    )
    if st.session_state["rekap_balok"]:
        beam_rows = []
        for kode_key, data in list(st.session_state["rekap_balok"].items()):
            beam_rows.append({
                "values": [
                    data["Kode balok"], f"{data['Bentang (mm)']:,} mm", data["Kondisi tumpuan"],
                    data["Dimensi (b × h)"], f"{data['Tinggi minimum (mm)']:,.0f} mm",
                    f"{data['Tinggi rekomendasi (mm)']:,.0f} mm", f"{data['Rasio b/h']:.3f}",
                    f"{data['Luas penampang (mm²)']:,} mm²",
                ],
                "clear": lambda k=kode_key: st.session_state["rekap_balok"].pop(k, None),
            })
        render_recap_table(
            st, key="pre-beam", title="Balok Pra-Desain",
            headers=["Kode", "Bentang", "Tumpuan", "Dimensi", "h minimum", "h rekomendasi", "Rasio b/h", "Luas penampang", "Aksi"],
            widths=[.7, .8, 1.15, .8, .8, .9, .65, 1.0, .6], rows=beam_rows,
        )
    if st.session_state["rekap_pelat"]:
        slab_rows = []
        for kode_key, data in list(st.session_state["rekap_pelat"].items()):
            slab_rows.append({
                "values": [
                    data["Kode panel"], data.get("Jenis pelat", data.get("Sistem", "Pelat")),
                    f"{data['Bentang acuan (mm)']:,} mm", data["Kondisi tumpuan"],
                    f"{data['h_min_mm']:.1f} mm", f"{data['Rekomendasi (mm)']:,} mm",
                    f"{data['Pilihan (mm)']:,} mm", data["Pemeriksaan"],
                ],
                "clear": lambda k=kode_key: st.session_state["rekap_pelat"].pop(k, None),
            })
        render_recap_table(
            st, key="pre-slab", title="Pelat Pra-Desain",
            headers=["Kode panel", "Jenis", "Bentang", "Tumpuan", "h minimum", "Rekomendasi", "Pilihan", "Status", "Aksi"],
            widths=[.75, 1.2, .8, 1.05, .75, .85, .7, 1.6, .6], rows=slab_rows,
        )
    if st.session_state["rekap_kolom"]:
        column_rows = []
        for kode_key, data in list(st.session_state["rekap_kolom"].items()):
            selection = data.get("Pilihan pengguna (mm)")
            dimension = f"{selection:,.0f} × {selection:,.0f} mm" if selection else "Belum dipilih"
            column_rows.append({
                "values": [
                    data["Kode kolom"], dimension, data["Rekomendasi VECTRION"],
                    f"{data['lu (mm)']:,.0f} mm", f"{data['Rasio kelangsingan']:.2f}",
                ],
                "clear": lambda k=kode_key: st.session_state["rekap_kolom"].pop(k, None),
            })
        render_recap_table(
            st, key="pre-column", title="Kolom Pra-Desain",
            headers=["Kode", "Dimensi pilihan", "Rekomendasi", "Panjang tak tertumpu", "Rasio kelangsingan", "Aksi"],
            widths=[.75, 1.0, 1.0, 1.0, 1.0, .6], rows=column_rows,
        )
    if st.session_state["rekap_analisis_etabs"]:
        etabs_rows = []
        for recap_key, data in list(st.session_state["rekap_analisis_etabs"].items()):
            etabs_rows.append({
                "values": [
                    data["DesignSect"], data["Story"],
                    format_kombinasi_tulangan(data.get("Ø atas 1 (mm)"), data.get("Jumlah atas 1", 0), data.get("Ø atas 2 (mm)"), data.get("Jumlah atas 2", 0)),
                    format_kombinasi_tulangan(data.get("Ø bawah 1 (mm)"), data.get("Jumlah bawah 1", 0), data.get("Ø bawah 2 (mm)"), data.get("Jumlah bawah 2", 0)),
                    status_kombinasi_balok(data),
                ],
                "clear": lambda k=recap_key: clear_etabs_beam_recap(st.session_state, k),
            })
        render_recap_table(
            st, key="post-beam", title="Balok Pasca-ETABS",
            headers=["Nama", "Story", "Kombinasi tulangan atas", "Kombinasi tulangan bawah", "Status", "Aksi"],
            widths=[.85, .8, 1.45, 1.45, .8, .6], rows=etabs_rows,
        )
    if st.session_state["rekap_analisis_etabs_kolom"]:
        column_rows = []
        for recap_key, data in list(st.session_state["rekap_analisis_etabs_kolom"].items()):
            column_rows.append({
                "values": [data["Kode"], data["Ukuran"], data["Kombinasi tulangan"],
                           f"{data['As tersedia (mm²)']:,.2f}", f"{data['Rasio aktual (%)']:.2f}%",
                           f"{data['As minimum (mm²)']:,.2f}", data["Status"]],
                "clear": lambda k=recap_key: clear_etabs_column_recap(st.session_state, k),
            })
        render_recap_table(
            st, key="post-column", title="Kolom Pasca-ETABS",
            headers=["Kode", "Ukuran", "Kombinasi tulangan", "As tersedia (mm²)", "Rasio aktual", "As minimum (mm²)", "Status", "Aksi"],
            rows=column_rows,
        )
    if not st.session_state["rekap_balok"] and not st.session_state["rekap_pelat"] and not st.session_state["rekap_kolom"] and not st.session_state["rekap_analisis_etabs"] and not st.session_state["rekap_analisis_etabs_kolom"]:
        st.caption("Belum ada hasil tersimpan. Rekap akan tetap tersedia selama sesi Streamlit.")
