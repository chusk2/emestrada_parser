import streamlit as st
import pandas as pd

CSV_PATH = "final_classification_chemistry.csv"

# wide mode
st.set_page_config(layout="wide")

st.title("Clasificación de ejercicios de química")

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

    for index, row in dataframe.iterrows():
        year = row["año"]
        subject = row["asignatura"]
        topic = row["tema"]
        exam = row["convocatoria"]
        exercise = row["ejercicio"]
        type_ = row["tipo de ejercicio"]

        output_string = f"{year} - {exam}, {exercise}\n"

        exercises.append(output_string)

    lines = [f"{subject.title()}\nTema: {topic}\nTipo de ejercicio: {type_}\n\n"]
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
