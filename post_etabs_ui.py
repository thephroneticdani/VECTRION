"""Streamlit pages for post-ETABS beam and column workflows."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from etabs_beam import (
    BAR_DIAMETERS_MM,
    format_kombinasi_tulangan,
    hitung_tulangan_balok,
    read_etabs_beam_summary,
    status_kebutuhan,
    status_kombinasi_balok,
    ukuran_dari_designsect,
)
from etabs_column import BAR_DIAMETERS_MM as COLUMN_BAR_DIAMETERS_MM, format_kombinasi_tulangan_kolom, hitung_tulangan_kolom
from recap import save_etabs_beam_recap, save_etabs_column_recap, clear_etabs_column_recap
from recap_table_ui import render_recap_table


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
        record = {
            "DesignSect": item["DesignSect"], "Story": item["Story"],
            "AsTopTotal maks.": top_required, "AsBotTotal maks.": bottom_required,
            "Ø atas 1 (mm)": d1, "Jumlah atas 1": int(n1),
            "Ø atas 2 (mm)": d2, "Jumlah atas 2": int(n2),
            "Ø bawah 1 (mm)": db1, "Jumlah bawah 1": int(nb1),
            "Ø bawah 2 (mm)": db2, "Jumlah bawah 2": int(nb2),
            **as_values, "Status atas": top_status, "Status bawah": bottom_status,
        }
        if st.button("Simpan ke Rekap", key=f"save_etabs_rebar_{ordinal}", type="primary"):
            save_etabs_beam_recap(st.session_state, record)
            st.success("Pilihan tulangan tersimpan di Rekap Tulangan Pasca-ETABS dan Rekap Analisis.")


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
        table_rows = []
        for data in recap.values():
            table_rows.append({
                "values": [
                    ukuran_dari_designsect(data["DesignSect"]),
                    data["Story"],
                    format_kombinasi_tulangan(data.get("Ø atas 1 (mm)"), data.get("Jumlah atas 1", 0), data.get("Ø atas 2 (mm)"), data.get("Jumlah atas 2", 0)),
                    format_kombinasi_tulangan(data.get("Ø bawah 1 (mm)"), data.get("Jumlah bawah 1", 0), data.get("Ø bawah 2 (mm)"), data.get("Jumlah bawah 2", 0)),
                    status_kombinasi_balok(data),
                ]
            })
        render_recap_table(
            st, key="post-etabs-summary", title="Rekap tulangan Pasca-ETABS",
            headers=["Ukuran", "Story", "Kombinasi tulangan atas", "Kombinasi tulangan bawah", "Status"],
            widths=[1.0, 0.9, 1.5, 1.5, 0.9], rows=table_rows, clear_column=False,
        )


def render_post_etabs_column(st):
    st.markdown("## Pasca-ETABS · Kolom")
    st.info(
        "Cek dasar luas tulangan longitudinal: target minimum 1–8% dari luas bruto penampang. "
        "Bukan desain kapasitas kolom; gaya aksial, momen, kelangsingan, sengkang, dan detailing tidak dihitung.",
        icon="ℹ️",
    )
    with st.form("post_etabs_column_form"):
        code = st.text_input("Kode kolom", value="K1", max_chars=40)
        dim_a, dim_b, dim_r = st.columns(3)
        width = dim_a.number_input("Lebar b (mm)", min_value=100, max_value=3000, value=400, step=10)
        depth = dim_b.number_input("Tinggi h (mm)", min_value=100, max_value=3000, value=400, step=10)
        ratio = dim_r.number_input("Target As minimum (%)", min_value=1.0, max_value=8.0, value=1.0, step=0.5)
        st.markdown("**Tulangan longitudinal — maksimal tiga kombinasi**")
        bar_cols = st.columns(3)
        diameters, quantities = [], []
        for index, column in enumerate(bar_cols, start=1):
            with column:
                st.caption(f"Kombinasi {index}")
                diameters.append(st.selectbox(f"Diameter {index} (mm)", COLUMN_BAR_DIAMETERS_MM, index=COLUMN_BAR_DIAMETERS_MM.index(16), key=f"post_column_d{index}"))
                quantities.append(st.number_input(f"Jumlah {index}", min_value=0, value=0, step=1, key=f"post_column_n{index}"))
        submitted = st.form_submit_button("Hitung As Kolom", type="primary")

    if submitted:
        try:
            code_value = code.strip()
            if not code_value:
                raise ValueError("Kode kolom wajib diisi.")
            result = hitung_tulangan_kolom(width, depth, ratio, diameters, quantities)
            st.session_state["draft_etabs_kolom"] = {
                "Kode": code_value,
                "Ukuran": f"{width:g}×{depth:g}",
                "b (mm)": float(width), "h (mm)": float(depth),
                "Diameter (mm)": list(diameters),
                "Jumlah": [int(value) for value in quantities],
                "Kombinasi tulangan": format_kombinasi_tulangan_kolom(diameters, quantities),
                **result,
            }
            st.session_state.pop("post_column_error", None)
        except ValueError as exc:
            st.session_state["post_column_error"] = str(exc)
    if st.session_state.get("post_column_error"):
        st.error(st.session_state["post_column_error"])

    draft = st.session_state.get("draft_etabs_kolom")
    if draft:
        st.markdown("### Hasil pemeriksaan As kolom")
        result_cols = st.columns(4)
        result_cols[0].metric("Luas penampang", f"{draft['Luas penampang (mm²)']:,.0f} mm²")
        result_cols[1].metric("As minimum", f"{draft['As minimum (mm²)']:,.2f} mm²")
        result_cols[2].metric("As tersedia", f"{draft['As tersedia (mm²)']:,.2f} mm²")
        result_cols[3].metric("Rasio aktual", f"{draft['Rasio aktual (%)']:.2f}%")
        if draft["Status"] == "Memenuhi":
            st.success("As tersedia berada di antara target minimum dan batas input 8%.")
        elif draft["Status"] == "Melebihi 8%":
            st.error("As tersedia melebihi batas maksimum 8% dari luas bruto.")
        else:
            st.error("As tersedia belum mencapai target minimum.")
        st.caption(f"{draft['Kode']} · {draft['Ukuran']} mm · {draft['Kombinasi tulangan']}")
        if st.button("Simpan ke Rekap", key="save_post_etabs_column", type="primary"):
            save_etabs_column_recap(st.session_state, draft)
            st.success("Hasil kolom tersimpan di Rekap Pasca-ETABS dan Rekap Analisis.")

    recap = st.session_state.get("rekap_etabs_kolom", {})
    if recap:
        st.markdown("### Rekap tulangan Pasca-ETABS · Kolom")
        rows = []
        for key, data in recap.items():
            rows.append({
                "values": [data["Kode"], data["Ukuran"], data["Kombinasi tulangan"],
                           f"{data['As tersedia (mm²)']:,.2f}", f"{data['Rasio aktual (%)']:.2f}%",
                           f"{data['As minimum (mm²)']:,.2f}", data["Status"]],
                "clear": lambda k=key: clear_etabs_column_recap(st.session_state, k),
            })
        render_recap_table(
            st, key="post-etabs-column", title="Rekap tulangan kolom",
            headers=["Kode", "Ukuran", "Kombinasi tulangan", "As tersedia (mm²)", "Rasio aktual", "As minimum (mm²)", "Status", "Aksi"],
            rows=rows,
        )
