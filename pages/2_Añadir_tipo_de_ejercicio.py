import json
import streamlit as st

## INITIALISE session_state keys
state = st.session_state

if not "run" in state.keys():
    state["run"] = 0

if "exercise_types_dict" not in state.keys():
    state["exercise_types_dict"] = {}

    with open('../data/exercise_types.json', 'r') as file:
        state["exercise_types_dict"] = json.load(file)

SUBJECTS = list(state["exercise_types_dict"].keys())

for key in ['subjects_key', 'topics_key', 'exercise_types_key']:
    if not key in state.keys():
        state[key] = []

if not "type_key" in state.keys():
    state["type"] = ""

def store_data():
    # retrieve data from current run
    current_subject = state['subject_key']
    current_topic   = state['topics_key']
    current_type    = state["type_key"]

    # add values to dictionary
    dictionary = state["exercise_types_dict"]
    dictionary[current_subject][current_topic].append(current_type)

    # reset widgets
    state['type_key'] = ""

def export_data():
    with open('../data/exercise_types.json', 'w') as file:
        json.dump(state["exercise_types_dict"], file)

def reload_topics():
    subject = state['subject_key']
    state["topics"] = list(state["exercise_types_dict"][subject].keys())

st.title("Añadir un nuevo tipo de ejercicio")

with st.form("form"):

    st.selectbox('Asignatura', options = SUBJECTS, key = "subject_key",
                 on_change=reload_topics)
    
    st.selectbox('Tema', options = state["topics"], key = "topics_key" )

    st.text_input('Tipo de ejercicio', max_chars=200, key = "type_key")

    st.form_submit_button('Guardar datos', on_click=store_data)

st.button("Exportar datos", on_click=export_data)
    


