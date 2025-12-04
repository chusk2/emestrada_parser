import streamlit as st
from PyPDF2 import PdfReader
from pathlib import Path

st.title('Classify exercise')

state = st.session_state

pdf_file = st.file_uploader('Add pdf file')

if pdf_file:
    reader = PdfReader(pdf_file)
    first_page = reader.pages[0]

    first_page_text = first_page.extract_text()
    exercises = []
    exams = ['Junio', 'Julio', 'Reserva 1', 'Reserva 2',
            'Reserva 3', 'Reserva 4', 'Septiembre']

    text = [line for line in first_page_text.split('\n') if line != '']
    for line in first_page_text.split('\n'):
        for exam in exams:
            if exam in line:
                exercises.append(line.strip(' ')[2:])
            if line.split():
                if line.split()[0] in ['FÍSICA', 'QUÍMICA', 'MATEMÁTICAS']:
                    state.subject = line

    topic_exercise_types = [f'integrales {type}' for type in ['cambio de variable', 'racional', 'por partes'] 
                            ]
    with st.form(key = 'form'):
        form_data = {
            'year' : int(pdf_file.name.split()[0]),
            'exercise' : st.selectbox('Exercise', options = exercises),
            'exercise_type' : st.selectbox('Tipo de ejercicio', options = topic_exercise_types,
                                           accept_new_options= True)
        }

        st.form_submit_button('Guardar datos')

    st.write(form_data)
    print(exercises[0])
# with st.form('form', key = 'form'):

#     form_data = {
#     'year' : st.selectbox('Año', options = range(2000, 2026)),

    



