import json
import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader

# list of subjects
SUBJECTS = ['FÍSICA', 'QUÍMICA', 'MATEMÁTICAS II',
            'MATEMÁTICAS APLICADAS A LAS CIENCIAS SOCIALES']

# list to store the exercises in the file
exercises = []

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

# after submit, store the data and reset the corresponding form widgets
def store_data():
    # store information into data dictionary
    state['data']['year']           .append(year)
    state['data']['subject']        .append(subject)
    state['data']['topic']          .append(topic)
    state['data']['exercise']       .append(state['exercise_key'])
    state['data']['exam']           .append(state['exercise_key'].split('.')[0])
    state['data']['exercise_type']  .append(state['exercise_type_key'])
    state['data']['statement']      .append(state['statement_key'])
    
    # reset the widgets from the form
    state["exercise_type_key"] = []
    state['statement_key'] = ""

# load the exercise types dictionary
with open('./data/exercise_types.json', 'r') as file:
    exercise_types_dict = json.load(file)

## START UI ##

st.title('Classify exercises')

pdf_file = st.file_uploader('Add pdf file', key = "pdf_form")

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
                subject = 'Mates CCSS'
            elif line == "MATEMÁTICAS II":
                subject = "Mates II"
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
        st.selectbox('Exercise', options = exercises, key = "exercise_key")
        st.multiselect('Tipo de ejercicio', options = exercise_types_list,
                                           key = "exercise_type_key")
        st.text_area('Insert exercise statement here', key = "statement_key")

        submitted  = st.form_submit_button('Guardar datos', on_click=store_data)

    if st.button('Save data into csv', key = "save_csv"):
        
        # start export process only when at least one exercise has been classified
        if len(state['data']['subject']) > 0:

            st.divider()
            st.write('Classification data for current exercise:')

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
            st.warning("There are no values stored to export to a csv file!")