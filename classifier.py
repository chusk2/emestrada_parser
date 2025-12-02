import streamlit as st
from PyPDF2 import PdfReader
import json

def get_exams(file):
    # Use the 'file' object that was passed as an argument
    pdf_reader = PdfReader(file)
    first_page = pdf_reader.pages[0]
    text = first_page.extract_text().split('\n')

    exams = []
    # Initialize variables to a default value before the loop
    # This prevents an UnboundLocalError if the PDF is malformed
    year, subject, topic = None, None, None

    for line in text:
        line = line.strip() # year, subject, and topic are defined in the loop but not initialized
        if line.startswith('20'):
            year = int(line)

        elif line in ['QUÍMICA', 'FISICA', 'MATEMÁTICAS']:
            if line == 'QUÍMICA':
                subject = 'QUIMICA'
            else:
                subject = line

        elif line.startswith('TEMA'):
            topic = line.split(': ')[1]

        elif line.startswith('•'):
            exams.append(line[2:])
        else:
            continue

    return year, subject, topic, exams


available_types = ['Alfa', 'Principio de LeChatelier',
                   'Concentraciones', 'Cinética',
                   'Equilibrio heterogéneo',
                   'En función de alfa']

st.title('Exercises classifier')

# --- Action Buttons ---
# Place buttons at the top. Their logic will run before the widgets are rendered.
col1, col2 = st.columns(2)

with col1:
    # We only show the save button if a file has been uploaded.
    # We check the session_state directly.
    if 'file_uploader' in st.session_state and st.session_state['file_uploader'] is not None:
        if st.button('Save classification', use_container_width=True):
            # This logic is now self-contained and uses session_state
            year, subject, topic, exams = get_exams(st.session_state['file_uploader'])
            all_results = []
            for index, exam in enumerate(exams):
                all_results.append({
                    'subject' : subject,
                    'year': year, 
                    'topic' : topic,
                    'exam': exam,
                    'type': st.session_state[f'multiselect_{index}']
                })

            filename = f"{subject}_{year}_{topic.replace(' ', '_')}.json"
            with open(f'./classified_json_files/{filename}', 'w') as f:
                json.dump(all_results, f, indent=4)
            st.success(f"Classification saved to:\n{filename}")

with col2:
    if st.button('Reset', use_container_width=True):
        # Find all keys related to the form and delete them
        keys_to_delete = ['file_uploader']
        for key in st.session_state.keys():
            if 'multiselect' in key:
                keys_to_delete.append(key)
        
        for key in keys_to_delete:
            if key in st.session_state:
                del st.session_state[key]

        # Rerun the app. On the next run, the widgets will be created in their default state.
        st.rerun()

# --- Main App UI ---
file = st.file_uploader('Upload an exams file', key='file_uploader')

if file:
    year, subject, topic, exams = get_exams(file)
    for index, exam in enumerate(exams):
        st.write(exam)
        st.multiselect(label = 'tipo ejercicio', options = available_types, key = f'multiselect_{index}')
