import pathlib
import streamlit as st

DARK = dict(
    bg="#0f1117", panel="#171b26", border="#2a2f3f",
    accent="#e8c547", accent2="#5fc4b8", text="#d4d8e8", muted="#7a8099",
)
LIGHT = dict(
    bg="#f5f6fa", panel="#ffffff", border="#d0d4e4",
    accent="#9a7c00", accent2="#1e8a80", text="#1a1d2e", muted="#5a6080",
)

_CSS = (pathlib.Path(__file__).parent / "styles.css").read_text()


def apply_theme():
    tv = DARK if st.session_state.theme == "dark" else LIGHT

    narrow_css = (
        ".block-container { max-width: 860px !important; "
        "padding-left: 2rem !important; padding-right: 2rem !important; }"
        if st.session_state.layout_mode == "narrow" else ""
    )

    st.html(
        f"<style>:root {{"
        f"--bg:{tv['bg']};--panel:{tv['panel']};--border:{tv['border']};"
        f"--accent:{tv['accent']};--accent2:{tv['accent2']};"
        f"--text:{tv['text']};--muted:{tv['muted']};--radius:8px;"
        f"}}{narrow_css}</style>"
        f"<style>{_CSS}</style>"
    )
