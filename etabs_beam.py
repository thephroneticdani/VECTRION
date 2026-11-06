"""ETABS beam summary import and basic provided-reinforcement checks."""

from __future__ import annotations

from collections import defaultdict
from math import pi, isfinite
from pathlib import Path
import re


REQUIRED_COLUMNS = {
    "story": "Story",
    "designsect": "DesignSect",
    "astoptotal": "AsTopTotal",
    "asbottotal": "AsBotTotal",
}
BAR_DIAMETERS_MM = (8, 10, 12, 13, 16, 19, 22, 25, 29, 32)


def _normalize_header(value):
    return re.sub(r"[^a-z0-9]", "", str(value or "").lower())


def _number(value, field, row_number):
    try:
        result = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Nilai {field} pada baris {row_number} bukan angka.") from None
    if not isfinite(result) or result < 0:
        raise ValueError(f"Nilai {field} pada baris {row_number} harus angka nol atau lebih.")
    return result


def read_etabs_beam_summary(file_obj):
    """Read an ETABS .xlsx beam summary, tolerating title/unit rows above headers."""
    try:
        from openpyxl import load_workbook
    except ImportError as exc:
        raise RuntimeError("Pembaca .xlsx belum tersedia. Pasang dependency openpyxl.") from exc

    name = getattr(file_obj, "name", "ETABS.xlsx")
    if Path(name).suffix.lower() != ".xlsx":
        raise ValueError("Format yang didukung saat ini hanya .xlsx.")
    try:
        if hasattr(file_obj, "seek"):
            file_obj.seek(0)
        workbook = load_workbook(file_obj, read_only=True, data_only=True)
    except Exception as exc:
        raise ValueError(f"File Excel tidak dapat dibaca: {exc}") from exc

    required = set(REQUIRED_COLUMNS)
    selected_sheet = None
    header_row = None
    columns = None
    for sheet in workbook.worksheets:
        for index, row in enumerate(sheet.iter_rows(min_row=1, max_row=30, values_only=True), start=1):
            found = {_normalize_header(value): col for col, value in enumerate(row)}
            if required.issubset(found):
                selected_sheet, header_row, columns = sheet, index, found
                break
        if selected_sheet is not None:
            break
    if selected_sheet is None:
        workbook.close()
        raise ValueError("Tidak ditemukan sheet dengan kolom Story, DesignSect, AsTopTotal, dan AsBotTotal.")

    units = {}
    unit_values = next(selected_sheet.iter_rows(min_row=header_row + 1, max_row=header_row + 1, values_only=True), ())
    for key, canonical in REQUIRED_COLUMNS.items():
        col_index = columns[key]
        units[canonical] = str(unit_values[col_index]).strip() if col_index < len(unit_values) and unit_values[col_index] else ""

    grouped = defaultdict(lambda: {"AsTopTotal": 0.0, "AsBotTotal": 0.0, "jumlah_data": 0})
    for row_number, row in enumerate(selected_sheet.iter_rows(min_row=header_row + 2, values_only=True), start=header_row + 2):
        vals = {}
        for key, canonical in REQUIRED_COLUMNS.items():
            ix = columns[key]
            vals[canonical] = row[ix] if ix < len(row) else None
        if all(value is None or str(value).strip() == "" for value in vals.values()):
            continue
        story, section = (str(vals[key] or "").strip() for key in ("Story", "DesignSect"))
        if not story or not section:
            continue
        top = _number(vals["AsTopTotal"], "AsTopTotal", row_number)
        bottom = _number(vals["AsBotTotal"], "AsBotTotal", row_number)
        item = grouped[(section, story)]
        item["AsTopTotal"] = max(item["AsTopTotal"], top)
        item["AsBotTotal"] = max(item["AsBotTotal"], bottom)
        item["jumlah_data"] += 1
    workbook.close()
    if not grouped:
        raise ValueError(f"Sheet '{selected_sheet.title}' tidak berisi baris desain balok yang valid.")
    rows = [
        {"DesignSect": section, "Story": story, **values}
        for (section, story), values in grouped.items()
    ]
    rows.sort(key=lambda item: (item["DesignSect"].casefold(), item["Story"].casefold()))
    return {"sheet": selected_sheet.title, "units": units, "rows": rows}


def area_tulangan_mm2(diameter_mm, quantity):
    """Return area of one/more round bars in mm², validating user inputs."""
    diameter = _number(diameter_mm, "diameter", "input")
    count = _number(quantity, "jumlah batang", "input")
    if diameter <= 0 or count < 0 or not count.is_integer():
        raise ValueError("Diameter harus lebih dari 0 mm dan jumlah batang bilangan bulat nol atau lebih.")
    return pi * diameter**2 / 4 * int(count)


def hitung_tulangan_balok(diameters_top, quantities_top, diameters_bottom, quantities_bottom):
    """Compute provided steel areas for up to two bar sizes at top and bottom."""
    if not all(len(values) == 2 for values in (diameters_top, quantities_top, diameters_bottom, quantities_bottom)):
        raise ValueError("Masukkan tepat dua pasangan diameter dan jumlah untuk sisi atas dan bawah.")
    top = sum(area_tulangan_mm2(d, n) for d, n in zip(diameters_top, quantities_top))
    bottom = sum(area_tulangan_mm2(d, n) for d, n in zip(diameters_bottom, quantities_bottom))
    return {"As atas tersedia (mm²)": top, "As bawah tersedia (mm²)": bottom}


def status_kebutuhan(as_provided, as_required):
    """A provided area equal to or greater than demand satisfies this simple check."""
    required = _number(as_required, "As perlu", "input")
    provided = _number(as_provided, "As tersedia", "input")
    return "Memenuhi" if provided >= required else "Tidak memenuhi"
