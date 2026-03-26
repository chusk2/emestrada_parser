import streamlit as st
import pandas as pd
from theme import apply_theme

CSV_PATH = "final_classification_chemistry.csv"

st.set_page_config(
    page_title="Selectividad Andalucía · Añadir ejercicio",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Session state defaults ---
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "layout_mode" not in st.session_state:
    st.session_state.layout_mode = "wide"
# dataframe to store new rows with exercises
if "new_rows_df" not in st.session_state:
    st.session_state.new_rows_df = pd.DataFrame()

apply_theme()

# --- Header row with toggle buttons ---
hdr_col, btn_col = st.columns([8, 2])

with hdr_col:
    st.markdown('<div class="main-header">Añadir Ejercicio · Selectividad</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Química · Andalucía · Añadir nuevo ejercicio al dataset</div>', unsafe_allow_html=True)

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

# --- Selectors to add a new row ---
st.markdown('<div class="filter-title">Nuevo ejercicio</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    years = sorted(df["year"].dropna().unique().tolist())
    selected_year = st.selectbox("Año", years)

with col2:
    subjects = sorted(df["subject"].dropna().unique().tolist())
    selected_subject = st.selectbox("Asignatura", subjects)

with col3:
    exams = sorted(df["exam"].dropna().unique().tolist())
    selected_exam = st.selectbox("Convocatoria", exams)

col4, col5, col6 = st.columns(3)

with col4:
    topics = sorted(df.loc[df["subject"] == selected_subject, "topic"].dropna().unique().tolist())
    selected_topic = st.selectbox("Tema", topics)

with col5:
    exercise_types = sorted(df.loc[df["topic"] == selected_topic, "exercise_type"].dropna().unique().tolist())
    selected_exercise_type = st.selectbox("Tipo de ejercicio", exercise_types)

with col6:
    selected_exercise = st.text_input("Ejercicio")


col1, col2 = st.columns(2)

# add exercise row
with col1:
    if st.button("Añadir ejercicio"):
        
        # ['year', 'subject', 'topic', 'exam', 'exercise', 'exercise_type']
        new_row = {
            "year": selected_year,
            "subject": selected_subject,
            "topic": selected_topic,
            "exam": selected_exam,
            "exercise": selected_exercise,
            "exercise_type": selected_exercise_type,
        }
        # TODO: append new_row to CSV_PATH
        
        st.session_state.new_rows_df = pd.concat(
            [st.session_state.new_rows_df, pd.DataFrame(new_row, index=[0])],
            ignore_index=True)
        st.success(f"Ejercicio añadido con éxito.")

# update csv file with new exercises
with col2:
    if st.button("Añadir ejercicios a csv"):
        
        original_df = pd.read_csv(CSV_PATH)
        updated_df = pd.concat([original_df, st.session_state.new_rows_df], ignore_index=True)

        # export to csv
        updated_df.to_csv(f"{CSV_PATH}_updated.csv", index = False)
        st.success(f"Archivo CSV actualizado con éxito.")    



