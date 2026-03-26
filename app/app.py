import streamlit as st
import pandas as pd
from theme import apply_theme

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

apply_theme()

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
