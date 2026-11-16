"""Build a standalone, print-ready HTML export of saved analysis recaps."""

from html import escape

from etabs_beam import format_kombinasi_tulangan


def _mm(value):
    return f"{value:,} mm" if isinstance(value, (int, float)) else str(value or "—")


def _dimension(entry):
    value = entry.get("Pilihan pengguna (mm)")
    return f"{value:,.0f} × {value:,.0f} mm" if value else "Belum dipilih"


def _slab_code(entry):
    return entry.get("Kode panel", entry.get("Kode", "—"))


def _slab_type(entry):
    return entry.get("Jenis pelat", entry.get("Sistem", "Pelat"))


def _ratio(entry):
    value = entry.get("Rasio kelangsingan")
    return f"{value:.2f}" if isinstance(value, (int, float)) else str(value or "—")


def _beam_top(entry):
    return format_kombinasi_tulangan(
        entry.get("Ø atas 1 (mm)"), entry.get("Jumlah atas 1", 0),
        entry.get("Ø atas 2 (mm)"), entry.get("Jumlah atas 2", 0),
    )


def _beam_bottom(entry):
    return format_kombinasi_tulangan(
        entry.get("Ø bawah 1 (mm)"), entry.get("Jumlah bawah 1", 0),
        entry.get("Ø bawah 2 (mm)"), entry.get("Jumlah bawah 2", 0),
    )


def _column_size(entry):
    width, height = entry.get("b (mm)"), entry.get("h (mm)")
    if isinstance(width, (int, float)) and isinstance(height, (int, float)):
        return f"{width:,.0f} × {height:,.0f} mm"
    value = str(entry.get("Ukuran", "")).strip()
    if not value:
        return "—"
    value = value.removesuffix("mm").strip().replace("×", " × ").replace("x", " × ")
    return f"{' '.join(value.split())} mm"


RECAP_SECTIONS = (
    ("Pra-Modelling — Balok", "rekap_balok", (
        ("Kode", lambda row: row.get("Kode balok", "—")),
        ("Bentang", lambda row: _mm(row.get("Bentang (mm)"))),
        ("Tumpuan", lambda row: row.get("Kondisi tumpuan", "—")),
        ("Dimensi", lambda row: row.get("Dimensi (b × h)", "—")),
    )),
    ("Pra-Modelling — Pelat", "rekap_pelat", (
        ("Kode", _slab_code),
        ("Jenis", _slab_type),
        ("Tumpuan", lambda row: row.get("Kondisi tumpuan", "—")),
        ("h pilihan", lambda row: _mm(row.get("Pilihan (mm)"))),
    )),
    ("Pra-Modelling — Kolom", "rekap_kolom", (
        ("Kode", lambda row: row.get("Kode kolom", "—")),
        ("Panjang tak tertumpu", lambda row: _mm(row.get("lu (mm)"))),
        ("Rasio kelangsingan", _ratio),
        ("Dimensi pilihan", _dimension),
    )),
    ("Pasca-Modelling — Balok", "rekap_analisis_etabs", (
        ("Nama", lambda row: row.get("DesignSect", "—")),
        ("Story", lambda row: row.get("Story", "—")),
        ("Kombinasi tulangan atas", _beam_top),
        ("Kombinasi tulangan bawah", _beam_bottom),
    )),
    ("Pasca-Modelling — Kolom", "rekap_analisis_etabs_kolom", (
        ("Kode", lambda row: row.get("Kode", "—")),
        ("Ukuran", _column_size),
        ("Kombinasi tulangan", lambda row: row.get("Kombinasi tulangan", "—")),
    )),
)


def build_recap_html(state):
    """Return a responsive HTML document containing every saved recap row."""
    sections = []
    for title, state_key, columns in RECAP_SECTIONS:
        entries = list(state.get(state_key, {}).values())
        if not entries:
            continue

        header_html = "".join(f"<th>{escape(label)}</th>" for label, _ in columns)
        row_html = []
        for entry in entries:
            cells = "".join(
                f"<td>{escape(str(getter(entry)))}</td>" for _, getter in columns
            )
            row_html.append(f"<tr>{cells}</tr>")
        sections.append(
            f"<section><h2>{escape(title)}</h2><div class='table-wrap'>"
            f"<table><thead><tr>{header_html}</tr></thead>"
            f"<tbody>{''.join(row_html)}</tbody></table></div></section>"
        )

    if not sections:
        sections.append("<p class='empty'>Belum ada hasil rekap tersimpan.</p>")

    return """<!doctype html>
<html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rekap Analisis VECTRION</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#e9ebee;color:#202329;font:15px/1.5 Arial,sans-serif}
main{max-width:1100px;margin:32px auto;padding:28px;background:#f4f5f7;border:1px solid #373c45;border-radius:9px}
header{display:flex;align-items:center;justify-content:space-between;gap:16px;border-bottom:2px solid #d6a63e;padding-bottom:16px}
h1{margin:0;color:#202329;font-size:26px}.print{border:0;border-radius:7px;background:#d6a63e;color:#17191d;padding:10px 16px;font-weight:700;cursor:pointer}
section{margin-top:26px}h2{font-size:19px;color:#272b32}.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:13px}
th,td{border:1px solid #d4d7dc;padding:8px;text-align:left;vertical-align:top;overflow-wrap:anywhere}
th{background:#e3e5e9;color:#202329}tbody tr:nth-child(even){background:#eaecf0}.empty{padding:20px 0;color:#626974}
@media(max-width:600px){main{margin:0;padding:16px;border:0;border-radius:0}header{align-items:flex-start;flex-direction:column}h1{font-size:22px}table{min-width:620px}}
@media print{@page{margin:12mm;size:landscape}body{background:#fff;color:#202329}main{max-width:none;margin:0;padding:0;border:0;border-radius:0;background:#fff}.print{display:none}section{break-inside:avoid}h2{break-after:avoid}th{background:#e3e5e9!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
</style></head><body><main><header><div><h1>Rekap Analisis VECTRION</h1>
<div>Structural Engineering Suite</div></div><button class="print" onclick="window.print()">Cetak / Simpan PDF</button></header>
__SECTIONS__</main></body></html>""".replace("__SECTIONS__", "".join(sections))
