import streamlit as st
from pathlib import Path
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
from styling import COLORS
from column_ui import render_column_module
from recap import beam_recap_warnings, slab_recap_summary, column_recap_summary
from engineering_disclaimer import render_engineering_disclaimer

inject_global_styles(st)

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

with st.sidebar:
    logo_path = Path(__file__).parent / "assets" / "vectrion_logo.png"
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
    else:
        st.markdown("## VECTRION")
    st.caption("Structural Engineering Suite")
    st.markdown("---")
    halaman_sidebar = st.radio(
        "Navigasi aplikasi", ["Beranda", "Pra-Desain", "Pasca-ETABS"],
        index=["Beranda", "Pra-Desain", "Pasca-ETABS"].index(st.session_state["halaman"]),
        key="sidebar_page",
    )
    if halaman_sidebar != st.session_state["halaman"]:
        navigate(st.session_state, halaman_sidebar)
    if st.session_state["halaman"] == "Pra-Desain":
        st.radio("Modul pra-desain", ["Balok", "Pelat", "Kolom"], horizontal=False, key="modul_pra")

st.title("VECTRION")
st.caption("Structural Engineering Suite · Pemeriksaan dimensi awal struktur beton bertulang")

def pindah(halaman):
    if "sidebar_page" in st.session_state:
        st.session_state["sidebar_page"] = halaman
    navigate(st.session_state, halaman)

if st.session_state["halaman"] == "Beranda":
    st.markdown("## Rekayasa struktur, dimulai dari pradesain")
    st.write("Pilih alur analisis untuk memulai pemeriksaan dimensi awal.")
    render_engineering_disclaimer(st)
    logo_path = Path(__file__).parent / "assets" / "vectrion_logo.png"
    if logo_path.exists():
        st.image(str(logo_path), width=440)
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
    st.markdown("## Analisis Pra-Desain")
    render_engineering_disclaimer(st)
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
            render_engineering_disclaimer(st)
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
    st.info("Belum tersedia")

# Rekap lintas halaman: tetap berada di session_state saat navigasi.
st.divider()
render_engineering_disclaimer(st)
st.markdown("### Rekap analisis")
if st.session_state["rekap_balok"]:
    st.markdown("**Balok**")
    for kode_key, data in list(st.session_state["rekap_balok"].items()):
        with st.container(key=f"rekap-card-balok-{kode_key}", border=True):
            data_col, action_col = st.columns([5, 1], vertical_alignment="center")
            data_col.markdown(f"**{data['Kode balok']}** · {data['Dimensi (b × h)']}")
            data_col.caption(f"Bentang {data['Bentang (mm)']} mm · Rasio b/h {data['Rasio b/h']:.3f} · Luas {data['Luas penampang (mm²)']:,} mm²")
            for warning in beam_recap_warnings(data):
                data_col.markdown(f"<span style=\"color:{COLORS['error']}\">{warning}</span>", unsafe_allow_html=True)
            if action_col.button("Clear", key=f"clear_balok_{kode_key}", use_container_width=True):
                del st.session_state["rekap_balok"][kode_key]
                st.rerun()
if st.session_state["rekap_pelat"]:
    st.markdown("**Pelat**")
    for kode_key, data in list(st.session_state["rekap_pelat"].items()):
        with st.container(key=f"rekap-card-pelat-{kode_key}", border=True):
            data_col, action_col = st.columns([5, 1], vertical_alignment="center")
            slab_title, slab_details, slab_warning = slab_recap_summary(data)
            data_col.markdown(f"**{slab_title}**")
            data_col.caption(slab_details)
            if slab_warning:
                data_col.markdown(f"<span style=\"color:{COLORS['error']}\">{slab_warning}</span>", unsafe_allow_html=True)
            if action_col.button("Clear", key=f"clear_pelat_{kode_key}", use_container_width=True):
                del st.session_state["rekap_pelat"][kode_key]
                st.rerun()
if st.session_state["rekap_kolom"]:
    st.markdown("**Kolom**")
    for kode_key, data in list(st.session_state["rekap_kolom"].items()):
        with st.container(key=f"rekap-card-kolom-{kode_key}", border=True):
            data_col, action_col = st.columns([5, 1], vertical_alignment="center")
            column_title, column_details = column_recap_summary(data)
            data_col.markdown(f"**{column_title}**")
            data_col.caption(column_details)
            if action_col.button("Clear", key=f"clear_kolom_{kode_key}", use_container_width=True):
                del st.session_state["rekap_kolom"][kode_key]
                st.rerun()
if not st.session_state["rekap_balok"] and not st.session_state["rekap_pelat"] and not st.session_state["rekap_kolom"]:
    st.caption("Belum ada hasil tersimpan. Rekap akan tetap tersedia selama sesi Streamlit.")
