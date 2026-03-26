import streamlit as st
import pandas as pd

CSV_PATH = "final_classification_chemistry.csv"

st.set_page_config(
    page_title="Selectividad Andalucía · Explorador",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Session state defaults ---
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "layout_mode" not in st.session_state:
    st.session_state.layout_mode = "wide"

# --- Theme palettes ---
DARK = dict(
    bg="#0f1117", panel="#171b26", border="#2a2f3f",
    accent="#e8c547", accent2="#5fc4b8", text="#d4d8e8", muted="#7a8099",
)
LIGHT = dict(
    bg="#f5f6fa", panel="#ffffff", border="#d0d4e4",
    accent="#9a7c00", accent2="#1e8a80", text="#1a1d2e", muted="#5a6080",
)

tv = DARK if st.session_state.theme == "dark" else LIGHT

narrow_css = (
    ".block-container { max-width: 860px !important; "
    "padding-left: 2rem !important; padding-right: 2rem !important; }"
    if st.session_state.layout_mode == "narrow" else ""
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

:root {{
    --bg:      {tv['bg']};
    --panel:   {tv['panel']};
    --border:  {tv['border']};
    --accent:  {tv['accent']};
    --accent2: {tv['accent2']};
    --text:    {tv['text']};
    --muted:   {tv['muted']};
    --radius:  8px;
}}

.stApp {{ background-color: var(--bg); }}

html, body, [class*="css"] {{
    font-family: 'Lora', Georgia, serif;
}}

/* Color our own prose elements; let Streamlit widget labels use their own theme */
p, li, td, th, .stMarkdown {{
    color: var(--text);
}}

section[data-testid="stSidebar"] {{
    background: var(--panel);
    border-right: 1px solid var(--border);
}}

.main-header {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.75rem;
    font-weight: 600;
    color: var(--accent);
    letter-spacing: -0.02em;
    margin: 0 0 0.15rem 0;
}}
.sub-header {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: var(--muted);
    letter-spacing: 0.05em;
    margin-bottom: 1.4rem;
}}

.filter-title {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent2);
    margin-bottom: 0.5rem;
}}

.metric-card {{
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.8rem 1rem;
    text-align: center;
}}
.metric-value {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.9rem;
    font-weight: 600;
    color: var(--accent);
    line-height: 1.1;
}}
.metric-label {{
    font-size: 0.7rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.2rem;
}}

.bar-row {{
    display: flex;
    align-items: center;
    margin-bottom: 0.45rem;
    gap: 0.6rem;
}}
.bar-label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--text);
    min-width: 180px;
    max-width: 180px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}
.bar-track {{
    flex: 1;
    height: 8px;
    background: var(--border);
    border-radius: 4px;
    overflow: hidden;
}}
.bar-fill {{
    height: 100%;
    background: linear-gradient(90deg, var(--accent2), var(--accent));
    border-radius: 4px;
}}
.bar-count {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    min-width: 22px;
    text-align: right;
}}
.dist-title {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.73rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--accent2);
    margin: 0.2rem 0 0.7rem 0;
}}

/* Compact toggle buttons */
div[data-testid="stHorizontalBlock"] button[kind="secondary"] {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    padding: 0.25rem 0.6rem;
    border-radius: 6px;
}}

#MainMenu {{ visibility: hidden; }}
footer    {{ visibility: hidden; }}
header    {{ visibility: hidden; }}

{narrow_css}
</style>
""", unsafe_allow_html=True)

# --- Header row with toggle buttons ---
hdr_col, btn_col = st.columns([8, 2])

with hdr_col:
    st.markdown('<div class="main-header">Explorador de Ejercicios · Selectividad</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Química · Andalucía · Ejercicios clasificados por tipo</div>', unsafe_allow_html=True)

with btn_col:
    st.markdown("<br>", unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        theme_label = "☀️ Light" if st.session_state.theme == "dark" else "🌙 Dark"
        if st.button(theme_label, key="toggle_theme"):
            st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
            st.rerun()
    with b2:
        layout_label = "◀ Narrow" if st.session_state.layout_mode == "wide" else "▶ Wide"
        if st.button(layout_label, key="toggle_layout"):
            st.session_state.layout_mode = "narrow" if st.session_state.layout_mode == "wide" else "wide"
            st.rerun()

@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH)

df = load_data()

# translate dataframe
translate_cols = {
    "year" : "año",
    "subject" : "asignatura",
    "topic" : "tema",
    "exam" : "convocatoria",
    "exercise" : "ejercicio",
    "exercise_type" : "tipo de ejercicio"
}

# format topic names
for topic in df.topic.dropna().unique():
    if topic:
        df.loc[df.topic == topic, "topic"] = topic.replace("_", " ").title()

# --- Filtros ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    subjects = sorted(df["subject"].dropna().unique().tolist())
    selected_subject = st.selectbox("Asignatura", subjects)

with col2:
    years = ["Todos"] + sorted(df["year"].dropna().unique().tolist())
    selected_year = st.selectbox("Año", years)

with col3:
    topics = ["Todos"] + sorted(df["topic"].dropna().unique().tolist())
    selected_topic = st.selectbox("Tema", topics)

with col4:
    if selected_topic != "Todos":
        exercise_types = ["Todos"] + sorted(
            df[df["topic"] == selected_topic]["exercise_type"].dropna().unique().tolist()
        )
    else:
        exercise_types = ["Todos"] + sorted(df["exercise_type"].dropna().unique().tolist())
    selected_exercise_type = st.selectbox("Tipo de ejercicio", exercise_types)

# --- Filtrado ---
filtered_df = df.copy()

filtered_df = filtered_df[filtered_df.subject == selected_subject]

if selected_year != "Todos":
    filtered_df = filtered_df[filtered_df.year == selected_year]

if selected_topic != "Todos":
    filtered_df = filtered_df[filtered_df["topic"] == selected_topic]

if selected_exercise_type != "Todos":
    filtered_df = filtered_df[filtered_df["exercise_type"] == selected_exercise_type]

st.caption(f"{len(filtered_df)} ejercicios encontrados")

filtered_translated = filtered_df.rename(columns=translate_cols)
st.dataframe(filtered_translated, hide_index=True, use_container_width=True)

def results_to_text(dataframe: pd.DataFrame) -> str:
    exercises = []

    subject = str(dataframe["asignatura"].dropna().iloc[0]).title() if not dataframe["asignatura"].dropna().empty else ""
    topic   = str(dataframe["tema"].dropna().iloc[0]) if not dataframe["tema"].dropna().empty else ""
    type_   = str(dataframe["tipo de ejercicio"].dropna().iloc[0]) if not dataframe["tipo de ejercicio"].dropna().empty else ""

    for _, row in dataframe.iterrows():
        year     = row["año"]
        exam     = row["convocatoria"]
        exercise = row["ejercicio"]
        output_string = f"{year} - {exam}, {exercise}\n"
        exercises.append(output_string)

    lines = [f"{subject}\nTema: {topic}\nTipo de ejercicio: {type_}\n\n"]
    lines.extend(exercises)
    return "".join(lines)

text_content = results_to_text(filtered_translated)
st.download_button(
    label="Descargar como texto",
    data=text_content,
    file_name="ejercicios_filtrados.txt",
    mime="text/plain",
)

# --- Barras de distribución por tipo de ejercicio ---
any_filter_active = any(v != "Todos" for v in [selected_year, selected_topic, selected_exercise_type])

counts = filtered_df["exercise_type"].dropna().value_counts()
if any_filter_active and not counts.empty:
    max_val = counts.max()
    bars_html = ""
    for label, cnt in counts.items():
        pct = int(cnt / max_val * 100)
        label = str(label)
        short = (label[:28] + "…") if len(label) > 28 else label
        bars_html += f"""
        <div class="bar-row">
          <span class="bar-label" title="{label}">{short}</span>
          <div class="bar-track"><div class="bar-fill" style="width:{pct}%"></div></div>
          <span class="bar-count">{cnt}</span>
        </div>"""
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="dist-title">Distribución por tipo de ejercicio</div>', unsafe_allow_html=True)
    st.markdown(bars_html, unsafe_allow_html=True)
