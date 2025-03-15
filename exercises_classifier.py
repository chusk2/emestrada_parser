
keywords = {
    'Equilibrio Químico': None,
    'Cantidad Química': None,
    'Ácido Base': None,

    'Conf. Electrónica': {
        'verdader' : 'Verdadero o Falso',
        'veracidad' : 'Verdadero o Falso',
        'radio' : 'Propiedades periódicas',
        'energía de ionización' : 'Propiedades periódicas',
        'afinidad electrónica' : 'Propiedades periódicas',
        'electronegatividad' : 'Propiedades periódicas',
        'primera energía de ionización' : 'Comparación energías de ionización',
        'Na+' : 'Radio / energía ionización Na+ y Ne',
        'estable' : 'Ion más estable',
        'números cuánticos' : 'Combinaciones de números cuánticos',
        'posibles' : 'Combinaciones de números cuánticos',
        'período' : 'Situar elementos en tabla periódica (grupo y período)',
        'energía reticular' : 'Ciclo de Born-Haber',
        'Br2 es líquido y el I2 es sólido' : 'Fuerzas de London',
        'agua es líquida' : 'Puentes de hidrógeno',
        'fusión' : 'Ecuación de Born-Landé',
        'dureza' : 'Ecuación de Born-Landé',
        'mayor energía reticular' : 'Ecuación de Born-Landé',

        
    },

    'Reactividad Orgánica': None,
    'Enlace Químico': {
        'verdader' : 'Verdadero o Falso',
        'veracidad' : 'Verdadero o Falso',
        'Lewis' : 'Estructuras de Lewis',
        'geometría' : 'Geometría según TRPECV',
        'ebullición' : 'Comparación del punto de ebullición',
        'hibridación' : 'Hibridación del átomo central',
        'nitrógeno y oxígeno' : 'Tipos enlace en N2 y O2',
        'sustancia' : 'Propiedades según tipo de enlace',


        
    },
    'Formulación': None,
    
    'Reacciones Redox': {
        'iónica y molecular' : 'Ajuste reacción redox',
        "método del ión-electrón" : "Ajuste reacción redox",
        "E*" : 'Pilas galvánicas',
        "E'" : 'Pilas galvánicas',
        'F = 96500 C' : 'Ley de Faraday'
    },

    'Solubilidad': {
        'verdader' : 'Verdadero o Falso',
        'veracidad' : 'Verdadero o Falso',
        'en agua' : 'Efecto ion común problema',
        'empiece a precipitar' : 'Cantidad a añadir para que precipite',
        'precipitado' : '¿Se formará precipitado?',
        ' M ': 'Efecto ion común problema',
        'pH' : 'Efecto del pH en la solubilidad',
    },

    'Termoquímica' : {
	'verdader' : 'Verdadero o Falso',
	'C-C': 'Entalpías de enlace',
	'S*' : 'Cálculo de entropía',
	"S'":  'Cálculo de entropía',
	'[' : 'Entalpías de formación',
	'a partir de los siguientes datos' : 'Ley de Hess',
	'a volumen constante' : 'Relación entalpía y energía interna',
	'trabajo' : '1er Principio de la Termodinámica',
	'interna' : '1er Principio de la Termodinámica',
	'entalpías de combustión' : 'Ley de Hess',
	'temperatura' : 'Energía libre de Gibbs teórico',
	}


}

def show_keywords():
    print('Select one option to show: ')
    topics = list(keywords.keys())
    
    options = ['1. List topics', '2. List exercise kinds', "3. Just enter '' to exit"]
    print(*options, sep='\n')
    
    selection = input('\nYour selection: ')
    print('\n')
    
    try:
        selection = int(selection)
        
        if selection == 1:
            print(f'\n- {topics[0]}\n- ', end='')
            print(*topics[1:], sep='\n- ')
        
        elif selection == 2:
            
            for index, topic in enumerate(topics):
                print(f'{index+1}. {topic}')
            print('\nSelect a topic: ')
            try:
                selection = int(input('Your selection: '))
                topic = topics[selection - 1]
                
                if keywords[topic] == None:
                    print('No keywords for this topic')
                else:
                    print(*keywords[topic].values(), sep='\n')                    

            except:
                print('Invalid selection for a topic')
        # empty selection means exit
        elif selection == '':
            return
        
    except Exception as e:
        print('Invalid selection')


def intro_keywords():
    with open('keywords.json', 'r') as f:
        keywords = json.load(f)
        
    while True:
        print('Los temas disponibles son:\n')
        print(*keywords.keys(), sep=', ')
        print('\n\n')
        topic = input('Introduce tema a rellenar: ')
        # check if topic is valid
        if topic not in keywords.keys():
            print('Tema no válido!\n\n')
            continue
        # topic exists
        break
    
    print(f'Añadiendo palabras clave para el tema {topic}\n\n')
    
    dict_ = {}
    # add keywords
    while True:
        keyword = input('Palabra clave: ')
        if keyword == '':
            break
        
        value = input('Tipo ejercicio: ')
        if keyword == '':
            break
        dict_[topic].update({keyword: value})
    
    # store the updated keywords
    keywords.update(dict_)
    with open('keywords.json', 'w') as f:
        json.dump(keywords, f, indent=4)


def classify_exercise_type(topic):
    keywords_topic = keywords[topic]
    # there are established keywords
    # for the current topic
    if keywords_topic:
        exercise_types = []
        subset = df[df.topic == topic]
        for statement in subset.statement:
            classified = False
            for k, v in keywords_topic.items():
                if k in statement:
                    exercise_types.append(v)
                    classified = True
                    break
            if not classified:
                exercise_types.append('varios')
    else:
        return pd.NA
    
    return exercise_types