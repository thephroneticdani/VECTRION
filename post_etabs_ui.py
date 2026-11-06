"""Streamlit pages for post-ETABS beam and column workflows."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from etabs_beam import BAR_DIAMETERS_MM, hitung_tulangan_balok, read_etabs_beam_summary, status_kebutuhan


POST_BEAM_DISCLAIMER = (
    "Perhitungan dasar balok: maksimal dua kombinasi diameter–jumlah di tepi atas dan bawah. "
    "Hanya cek luas As, bukan desain atau verifikasi kapasitas lengkap."
)


def _render_beam_row(item, units, ordinal):
    row_key = f"{item['DesignSect']}|{item['Story']}"
    key_prefix = f"etabs_rebar_{ordinal}"
    area_unit = units.get("AsTopTotal") or "mm²"
    with st.expander(f"{item['DesignSect']} · {item['Story']}", expanded=False):
        st.caption(
            f"As atas perlu: {item['AsTopTotal']:,.2f} {area_unit} · "
            f"As bawah perlu: {item['AsBotTotal']:,.2f} {area_unit} · "
            f"{item['jumlah_data']} baris station/kombinasi digabungkan"
        )
        st.markdown("**Tulangan atas**")
        a, b, c, d = st.columns(4)
        d1 = a.selectbox("Ø atas 1 (mm)", BAR_DIAMETERS_MM, index=BAR_DIAMETERS_MM.index(16), key=f"{key_prefix}_td1")
        n1 = b.number_input("Jumlah atas 1", min_value=0, value=0, step=1, key=f"{key_prefix}_tn1")
        d2 = c.selectbox("Ø atas 2 (mm)", BAR_DIAMETERS_MM, index=BAR_DIAMETERS_MM.index(16), key=f"{key_prefix}_td2")
        n2 = d.number_input("Jumlah atas 2", min_value=0, value=0, step=1, key=f"{key_prefix}_tn2")
        st.markdown("**Tulangan bawah**")
        a, b, c, d = st.columns(4)
        db1 = a.selectbox("Ø bawah 1 (mm)", BAR_DIAMETERS_MM, index=BAR_DIAMETERS_MM.index(16), key=f"{key_prefix}_bd1")
        nb1 = b.number_input("Jumlah bawah 1", min_value=0, value=0, step=1, key=f"{key_prefix}_bn1")
        db2 = c.selectbox("Ø bawah 2 (mm)", BAR_DIAMETERS_MM, index=BAR_DIAMETERS_MM.index(16), key=f"{key_prefix}_bd2")
        nb2 = d.number_input("Jumlah bawah 2", min_value=0, value=0, step=1, key=f"{key_prefix}_bn2")

        as_values = hitung_tulangan_balok([d1, d2], [n1, n2], [db1, db2], [nb1, nb2])
        top_required, bottom_required = item["AsTopTotal"], item["AsBotTotal"]
        top_status = status_kebutuhan(as_values["As atas tersedia (mm²)"], top_required)
        bottom_status = status_kebutuhan(as_values["As bawah tersedia (mm²)"], bottom_required)
        result_cols = st.columns(2)
        for column, label, result_key, required, status in (
            (result_cols[0], "As atas tersedia", "As atas tersedia (mm²)", top_required, top_status),
            (result_cols[1], "As bawah tersedia", "As bawah tersedia (mm²)", bottom_required, bottom_status),
        ):
            color = "#39744A" if status == "Memenuhi" else "#B33A32"
            column.markdown(
                f"<div style='border:1px solid {color};border-radius:10px;padding:.7rem 1rem'>"
                f"<b>{label}</b><br><span style='font-size:1.25rem'>{as_values[result_key]:,.2f} mm²</span>"
                f"<br><small>Perlu {required:,.2f} {area_unit} · "
                f"<b style='color:{color}'>{status}</b></small></div>",
                unsafe_allow_html=True,
            )
        st.caption("As tersedia = jumlah (π × Ø² / 4 × banyak batang), dihitung terpisah untuk atas dan bawah.")
        st.session_state.setdefault("rekap_etabs_balok", {})[row_key] = {
            "DesignSect": item["DesignSect"], "Story": item["Story"],
            "AsTopTotal maks.": top_required, "AsBotTotal maks.": bottom_required,
            **as_values, "Status atas": top_status, "Status bawah": bottom_status,
        }


def render_post_etabs_beam(st):
    st.markdown("## Pasca-ETABS · Balok")
    st.info(POST_BEAM_DISCLAIMER, icon="ℹ️")
    st.write("Unggah ringkasan desain balok ETABS berformat `.xlsx` untuk melihat kebutuhan As tiap DesignSect dan story.")
    with st.form("upload_etabs_beam_form"):
        upload = st.file_uploader("File ringkasan ETABS (.xlsx)", type=["xlsx"], key="etabs_beam_upload")
        submitted = st.form_submit_button("Baca Excel", type="primary")
    if submitted:
        if upload is None:
            st.error("Pilih file Excel terlebih dahulu.")
        else:
            try:
                result = read_etabs_beam_summary(upload)
                st.session_state["etabs_beam_summary"] = result
                st.session_state["rekap_etabs_balok"] = {}
                st.success(f"Sheet '{result['sheet']}' dibaca: {len(result['rows'])} kombinasi DesignSect/story.")
            except (ValueError, RuntimeError) as exc:
                st.error(str(exc))
    result = st.session_state.get("etabs_beam_summary")
    if not result:
        st.caption("Belum ada file ETABS yang dibaca.")
        return

    st.markdown("### Ringkasan kebutuhan tulangan")
    st.dataframe(
        pd.DataFrame(result["rows"])[["Story", "DesignSect", "AsTopTotal", "AsBotTotal"]].rename(
            columns={"AsTopTotal": "AsTopTotal maks.", "AsBotTotal": "AsBotTotal maks."}
        ),
        hide_index=True, width="stretch",
    )
    if st.button("Hitung Tulangan", key="toggle_etabs_rebar", type="primary"):
        st.session_state["show_etabs_rebar"] = not st.session_state.get("show_etabs_rebar", False)
    if st.session_state.get("show_etabs_rebar", False):
        st.markdown("### Pilihan tulangan dan pemeriksaan As")
        st.caption("Setiap baris mewakili satu DesignSect pada satu story. Maksimal dua kombinasi diameter–jumlah untuk masing-masing tepi atas dan bawah.")
        for index, item in enumerate(result["rows"]):
            _render_beam_row(item, result["units"], index)
    recap = st.session_state.get("rekap_etabs_balok", {})
    if recap:
        st.markdown("### Rekap tulangan Pasca-ETABS")
        st.dataframe(pd.DataFrame(recap.values()), hide_index=True, width="stretch")


def render_post_etabs_column(st):
    st.markdown("## Pasca-ETABS · Kolom")
    st.info("Coming soon — perhitungan kolom Pasca-ETABS belum tersedia.", icon="🏗️")
