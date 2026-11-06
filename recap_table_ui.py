"""Compact conventional-style recap tables with per-row clear buttons."""

from html import escape


def render_recap_table(st, *, key, title, headers, rows, widths, clear_column=True):
    """Render aligned desktop columns and readable label/value pairs on phones."""
    if not rows:
        return
    st.markdown(f"**{escape(str(title))}**")
    with st.container(key=f"recap-grid-{key}-header"):
        header_cells = st.columns(widths, vertical_alignment="center", gap="small")
        for cell, label in zip(header_cells, headers):
            cell.markdown(
                f"<div class='vx-recap-header'>{escape(str(label))}</div>",
                unsafe_allow_html=True,
            )
    for index, row in enumerate(rows):
        with st.container(key=f"recap-grid-{key}-row-{index}"):
            cells = st.columns(widths, vertical_alignment="center", gap="small")
            value_cells = cells[:-1] if clear_column else cells
            for cell, label, value in zip(value_cells, headers, row["values"]):
                cell.markdown(
                    "<div class='vx-recap-cell'>"
                    f"<span class='vx-recap-mobile-label'>{escape(str(label))}</span>"
                    f"<span class='vx-recap-value'>{escape(str(value))}</span>"
                    "</div>",
                    unsafe_allow_html=True,
                )
            if clear_column and cells[-1].button("Clear", key=f"clear-{key}-{index}", use_container_width=True):
                row["clear"]()
                st.rerun()
