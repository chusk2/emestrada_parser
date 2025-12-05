import streamlit as st
from PyPDF2 import PdfReader
from pathlib import Path
import json
import pandas as pd

# list of subjects
SUBJECTS = ['FÍSICA', 'QUÍMICA', 'MATEMÁTICAS II',
            'MATEMÁTICAS APLICADAS A LAS CIENCIAS SOCIALES']

# list to store the exercises in the file
exercises = []

# dictionary to store the classification data for each exercise
state = st.session_state
state['data'] = {key : [] for key in ['subject', 'year', 'topic', 'exam',
                               'exercise', 'exercise_type', 'statement']}

# load the exercise types dictionary
with open('exercise_types.json', 'r') as file:
    exercise_types_dict = json.load(file)

st.title('Classify exercise')

state = st.session_state

pdf_file = st.file_uploader('Add pdf file')

if pdf_file:

    # read the pdf file
    reader = PdfReader(pdf_file)

    # extract text from first page
    first_page = reader.pages[0]
    text = first_page.extract_text()
    text = [i.strip() for i in text.split('\n') if i != ' ']
    
    # parse the text to extract information
    for line in text:
        if line.startswith('2'):
            year = int(line)

        elif line in SUBJECTS:
            if line == 'MATEMÁTICAS APLICADAS A LAS CIENCIAS SOCIALES':
                subject = 'Matemáticas CCSS'
            else:
                subject = line.title()

        elif line.startswith('TEMA'):
            topic = line.split(': ')[1].title() 
        
        elif line.startswith('•'):
            line = line[2:].replace(',', '.')
            exercises.append(line)

    # get the list of exercise types for the current topic
    exercise_types_list = exercise_types_dict[subject][topic]
    
    st.write(f'### Classify exercises for *{topic}* from year **{year}**')

    with st.form(key = 'form'):
        form_data = {
            'exercise' : st.selectbox('Exercise', options = exercises),
            'exercise_type' : st.multiselect('Tipo de ejercicio', options = exercise_types_list),
            'statement' : st.text_area('Insert exercise statement here')
        }

        st.form_submit_button('Guardar datos')
    
    # add the data for current exercise to classification data dictionary
    classification_data = {
        'year' : year,
        'subject' : subject,
        'topic' : topic,
        'exercise' : form_data['exercise'],
        'exercise_type' : form_data['exercise_type'],
        'statement' : form_data['statement']
    }

    for key, value in classification_data.items():
        state['data'][key].append(value)
    
    st.write(state['data'])
    # columns for csv file: subject,year,topic,exam,type
    st.write('Classification data for current exercise:')
    st.write(form_data)
    st.write(len(state['data']))
    if st.button('Export data'):
        # csv columns:
        # subject,year,topic,exam,exercise,exercise_type,statement
        df = pd.read_csv('data.csv')
        classified_df = pd.DataFrame(state['data'], index = range(len(state['data'])))
        df = pd.concat([df, classified_df]).drop_duplicates()

    
