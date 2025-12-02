# %%
import pandas as pd
import json
import os
from pyuca import Collator

os.chdir('./classified_json_files')
json_files_unsorted = [file for file in os.listdir('.') if file.endswith('.json')]
json_files = sorted(json_files_unsorted, key=Collator().sort_key)

processed_files_text = 'processed_json_files.txt'
csv_file = 'classified_exercises.csv'

# store the processed json files into a text file
if os.path.exists(processed_files_text):
    with open(processed_files_text, 'r') as file:
        already_processed_json_files = [line.strip() for line in file.readlines()]
        json_files = [f for f in json_files if f not in already_processed_json_files]       

# add dataframes only if there are not processed files
if json_files:
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
    else:
        df = pd.DataFrame()

    for file in json_files:
        df = pd.concat([df, pd.read_json(file)])

    df = df.explode('type')

    df.to_csv(csv_file, index = False)

    # store the list of processed json files
    with open(processed_files_text, 'a') as file:
        for f in json_files:
            file.write(f'{f}\n')
    
    print(f'Added {len(json_files)} new files.')

else:
    print('There are not new files to add.')