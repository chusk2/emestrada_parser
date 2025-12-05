import streamlit as st
from PyPDF2 import PdfReader
from pathlib import Path
import json

SUBJECTS = ['FÍSICA', 'QUÍMICA', 'MATEMÁTICAS II',
            'MATEMÁTICAS APLICADAS A LAS CIENCIAS SOCIALES']

exercises = []


st.title('Classify exercise')

state = st.session_state

pdf_file = st.file_uploader('Add pdf file')

if pdf_file:
    reader = PdfReader(pdf_file)
    first_page = reader.pages[0]

    text = first_page.extract_text()
    exercises = []
    

    text = [i.strip() for i in text.split('\n') if i != ' ']
    
    

    for line in text:
        if line in subjects:
            if line == 'MATEMÁTICAS APLICADAS A LAS CIENCIAS SOCIALES':
                subject = 'Matemáticas CCSS'
            else:
                subject = line.title()

        elif line.startswith('TEMA'):
            topic = line.split(': ')[1].capitalize() 
        
        elif line.startswith('•'):
            line = line[2:].replace(',', '.')
            exercises.append(line)

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

    



