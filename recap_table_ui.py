"""Responsive HTML recap tables with Streamlit row-clear controls."""

from html import escape


def render_recap_table(st, *, key, title, headers, rows, widths=None, clear_column=True):
    """Render a semantic table on desktop and label/value cards on mobile."""
    if not rows:
        return

    value_headers = headers[:-1] if clear_column else headers
    st.markdown(f"**{escape(str(title))}**")

    table_rows = []
    for row in rows:
        cells = []
        for label, value in zip(value_headers, row["values"]):
            cells.append(
                "<td><span class='vx-recap-mobile-label'>"
                f"{escape(str(label))}</span><span class='vx-recap-value'>"
                f"{escape(str(value))}</span></td>"
            )
        table_rows.append("<tr>" + "".join(cells) + "</tr>")

    html = (
        "<div class='vx-recap-table-wrap'><table class='vx-recap-table'>"
        "<thead><tr>"
        + "".join(f"<th scope='col'>{escape(str(label))}</th>" for label in value_headers)
        + "</tr></thead><tbody>"
        + "".join(table_rows)
        + "</tbody></table></div>"
    )
    st.markdown(html, unsafe_allow_html=True)

    if clear_column:
        with st.container(key=f"recap-actions-{key}"):
            for index, row in enumerate(rows):
                descriptor = " · ".join(str(value) for value in row["values"][:2])
                label = f"Clear — {descriptor}" if descriptor else "Clear"
                if st.button(label, key=f"clear-{key}-{index}"):
                    row["clear"]()
                    st.rerun()
