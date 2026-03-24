import streamlit as st
import pandas as pd

CSV_PATH = "final_classification_chemistry.csv"

st.set_page_config(
    page_title="Selectividad Andalucía · Explorador",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

:root {
    --bg:      #0f1117;
    --panel:   #171b26;
    --border:  #2a2f3f;
    --accent:  #e8c547;
    --accent2: #5fc4b8;
    --text:    #d4d8e8;
    --muted:   #7a8099;
    --radius:  8px;
}

.stApp { background-color: var(--bg); }

html, body, [class*="css"] {
    font-family: 'Lora', Georgia, serif;
    color: var(--text);
}

section[data-testid="stSidebar"] {
    background: var(--panel);
    border-right: 1px solid var(--border);
}

.main-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.75rem;
    font-weight: 600;
    color: var(--accent);
    letter-spacing: -0.02em;
    margin: 0 0 0.15rem 0;
}
.sub-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: var(--muted);
    letter-spacing: 0.05em;
    margin-bottom: 1.4rem;
}

.filter-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent2);
    margin-bottom: 0.5rem;
}

.metric-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.8rem 1rem;
    text-align: center;
}
.metric-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.9rem;
    font-weight: 600;
    color: var(--accent);
    line-height: 1.1;
}
.metric-label {
    font-size: 0.7rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.2rem;
}

.bar-row {
    display: flex;
    align-items: center;
    margin-bottom: 0.45rem;
    gap: 0.6rem;
}
.bar-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--text);
    min-width: 180px;
    max-width: 180px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.bar-track {
    flex: 1;
    height: 8px;
    background: var(--border);
    border-radius: 4px;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent2), var(--accent));
    border-radius: 4px;
}
.bar-count {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    min-width: 22px;
    text-align: right;
}
.dist-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.73rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--accent2);
    margin: 0.2rem 0 0.7rem 0;
}

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">Explorador de Ejercicios · Selectividad</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Química · Andalucía · Ejercicios clasificados por tipo</div>', unsafe_allow_html=True)

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
col1, col2 = st.columns(2)

with col1:

    topics = ["Todos"] + sorted(df["topic"].dropna().unique().tolist())
    selected_topic = st.selectbox("Topic", topics)

with col2:
    if selected_topic != "Todos":
        exercise_types = ["Todos"] + sorted(
            df[df["topic"] == selected_topic]["exercise_type"].dropna().unique().tolist()
        )
    else:
        exercise_types = ["Todos"] + sorted(df["exercise_type"].dropna().unique().tolist())
    selected_exercise_type = st.selectbox("Exercise type", exercise_types)

# --- Filtrado ---
filtered = df.copy()

if selected_topic != "Todos":
    filtered = filtered[filtered["topic"] == selected_topic]
if selected_exercise_type != "Todos":
    filtered = filtered[filtered["exercise_type"] == selected_exercise_type]

st.caption(f"{len(filtered)} ejercicios encontrados")

# translate columns
filtered_translated = filtered.rename(columns=translate_cols)
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

# download button
text_content = results_to_text(filtered_translated)
st.download_button(
    label="Descargar como texto",
    data=text_content,
    file_name="ejercicios_filtrados.txt",
    mime="text/plain",
)

# --- Barras de distribución por tipo de ejercicio ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="dist-title">Distribución por tipo de ejercicio</div>', unsafe_allow_html=True)

counts = filtered["exercise_type"].dropna().value_counts()
if not counts.empty:
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
    st.markdown(bars_html, unsafe_allow_html=True)
else:
    st.markdown('<span style="color:var(--muted);font-size:0.75rem">Sin datos</span>', unsafe_allow_html=True)
