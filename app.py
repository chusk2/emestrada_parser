import pandas as pd
import streamlit as st

df = pd.read_csv('data.csv')

st.header('Ejercicios de Selectividad')

subjects = sorted(df.subject.unique())

topics = {}
for s in subjects:
    topics[s] = sorted(df[df.subject == s].topic.unique())

# temas = {
#     'Mates II' : ['Funciones', 'Geometría',
#     'Integrales', 'Matrices y Determinantes',
#     'Probabilidad', 'Sistemas de Ecuaciones Lineales'],
    
#     'Física' : ['Trabajo y Energía', 'Campo gravitatorio',
#                 'Campo eléctrico', 'Campo magnético',
#                 'Inducción magnética', 'Movimiento armónico simple',
#                 'Movimiento ondulatorio', 'Óptica', 'Física cuántica y nuclear'],

#     'Mates CCSS' : ['Funciones', 'Matrices', 'Sistemas de ecuaciones lineales',
#                     'Programación lineal', 'Probabilidad', 'Inferencia estadística' ]
# }

subject = st.sidebar.selectbox(label = 'Elige asignatura',
                     options = subjects)

if subject:
    df_filtered = df[df.subject == subject]
    
    # year
    years = sorted(df_filtered.year.unique(), reverse = True) 
    year = st.sidebar.selectbox(label = 'Elige año', options = years)

    if not st.sidebar.toggle('Todos los años'):
        df_filtered = df_filtered[df_filtered.year == year]

    topics = sorted(df_filtered.topic.unique())
    topic= st.sidebar.selectbox(label = 'Elige tema', options = topics)
    
    if topic:

        if not st.sidebar.toggle('Todos los temas'):
            df_filtered = df_filtered[df_filtered.topic == topic]

        # tipos de ejercicio
        exercise_types = sorted(df_filtered.exercise_type.unique())
        exercise_type = st.sidebar.selectbox(label = 'Tipo de ejercicio', options = exercise_types)

        if exercise_type:
            if not st.sidebar.toggle('Todos los tipos de ejercicio'):
                df_filtered = df_filtered[df_filtered.exercise_type == exercise_type]
        
        
    df_filtered = df_filtered.sort_values('year', ascending=False)
    df_filtered.reset_index(drop = True, inplace= True)
    df_filtered.index = df_filtered.index + 1
    # drop statement column
    cols = [i for i in df_filtered.columns if i != 'statement']
    st.write(df_filtered[cols])        


else:
    st.write(df)
