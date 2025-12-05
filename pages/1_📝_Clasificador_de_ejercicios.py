import json
import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader

# list of subjects
SUBJECTS = ['FÍSICA', 'QUÍMICA', 'MATEMÁTICAS II',
            'MATEMÁTICAS APLICADAS A LAS CIENCIAS SOCIALES']

## INITIALISE THE session_state keys

state = st.session_state

# dictionary to store the classification data for each exercise
if 'data' not in state:
    state['data'] = {key : [] for key in ['subject', 'year', 'topic', 'exam',
                                   'exercise', 'exercise_type', 'statement']}
    
if not "exercise_type_key" in state.keys():
    state["exercise_type_key"] = []

if not "statement_key" in state.keys(): 
    state['statement_key'] = ""

if not "pdf_file" in state.keys():
    state['pdf_file'] = None

if not 'exercises' in state.keys():
    state['exercises'] = []

if not 'subject' in state.keys():
    state['subject'] = ""

if not 'year' in state.keys():
    state['year'] = None

if not 'topic' in state.keys():
    state['topic'] = ""

# after submit, store the data and reset the corresponding form widgets
def store_data():
    # store information into data dictionary
    state['data']['year']           .append(state['year'])
    state['data']['subject']        .append(state['subject'])
    state['data']['topic']          .append(state['topic'])
    state['data']['exercise']       .append(state['exercise_key'])
    state['data']['exam']           .append(state['exercise_key'].split('.')[0])
    state['data']['exercise_type']  .append(state['exercise_type_key'])
    state['data']['statement']      .append(state['statement_key'])
    
    # reset the widgets from the form
    state["exercise_type_key"] = []
    state['statement_key'] = ""

def erase_data():
    state['data'] = {}


# load the exercise types dictionary
with open('./data/exercise_types.json', 'r') as file:
    exercise_types_dict = json.load(file)

## START UI ##

st.title('Clasificar ejercicios')

pdf_file = st.file_uploader('Carga un archivo PDF', key = "pdf_form")

if pdf_file:

    # read the pdf file
    reader = PdfReader(pdf_file)

    # extract text from first page
    first_page = reader.pages[0]
    text = first_page.extract_text()
    text = [i.strip() for i in text.split('\n') if i != ' ']
    
    ## parse the text to extract information
    
    # extract exercises if file has just been uploaded
    if not state['exercises']:
        for index, line in enumerate(text):
            for exam in ['junio', 'julio', 'septiembre', 'reserva']:
                if exam in line.lower():
                    pos = line.index(exam.title())
                    state['exercises'].append( line[pos:].strip() )
                    text.pop(index)
                    break

    # extract information of year and subject      
    for line in text:
        if line.startswith('2'):
            state['year'] = int(line)

        elif line in SUBJECTS:
            if line == 'MATEMÁTICAS APLICADAS A LAS CIENCIAS SOCIALES':
                subject = 'Mates CCSS'
            elif line == "MATEMÁTICAS II":
                subject = "Mates II"
            else:
                subject = line.title()
            
            state['subject'] = subject

        elif line.startswith('TEMA'):
            state['topic'] = line.split(': ')[1].title()

            # hard code an expection:
            # "reactividad orgánica" is called "orgánica"
            if state['topic'] == "Orgánica":
                state['topic'] = "Reactividad Orgánica"

    # get the list of exercise types for the current topic
    exercise_types_list = exercise_types_dict[state['subject']][state['topic']]
    
    st.write(f'### *{state['topic']}* (**{state['year']}**)')

    with st.form(key = 'form'):
        
        st.selectbox('Ejercicio', options = state['exercises'], key = "exercise_key")

        if not exercise_types_list:
            st.warning('No existe aún información sobre los tipos de ejercicio para este tema.')
            st.form_submit_button('Guardado de datos deshabilitado')

        else:
            st.multiselect('Tipo de ejercicio', options = exercise_types_list,
                                           key = "exercise_type_key")
        
            st.text_area('Enunciado', key = "statement_key")

            submitted  = st.form_submit_button('Guardar datos', on_click=store_data)

    col1, col2 = st.columns([1,1])

    with col1:
        if st.button('Exportar datos a CSV', key = "save_csv"):
            
            # start export process only when at least one exercise has been classified
            if len(state['data']['subject']) > 0:

                st.divider()
                st.write('Datos que serán añadidos al archivo principal de clasificiones:')

                # create dataframe from classification data
                classified_df = pd.DataFrame(state['data'], index = range(len(state['data']['subject'])))
                # explode exercise_type column
                classified_df = classified_df.explode('exercise_type')
                # show the classified data as dataframe
                st.write(classified_df)

                # merge the classification dataset to existing data
                df = pd.read_csv('./data/data.csv')
                df = pd.concat([df, classified_df]).drop_duplicates()
                
            else:
                st.warning("No hay clasificaciones guardadas para poder ser exportadas a CSV")
    
    with col2:
        # button to reset all stored classifications
        # USE WITH CAUTION. WORK WILL BE LOST WHEN CLICKED
        st.button('Borrar clasificaciones guardadas', on_click = erase_data)