# Codebase Report

Based on my analysis, here's a report on your codebase:

The project is a data processing pipeline that classifies university entrance exam exercises from PDF files. Here's a breakdown of the key files and their roles:

- **Data Acquisition:**
    - `emestrada_crawler.ipynb`: A Jupyter notebook that downloads Physics exercises in PDF format from the website `emestrada.org`.

- **Data Extraction:**
    - `parser.ipynb`: This notebook is the heart of the data extraction process. It uses OCR (Tesseract) to extract text from the PDF files and organizes it into unclassified CSV files within the `csv/` directory.

- **Classification:**
    - `keywords.json`: This file is crucial for classification, as it contains the keywords for each exercise type.
    - `exercises_classifier.py`: This script contains the logic for classifying exercises based on the keywords.
    - `test_classifier.ipynb`: This notebook applies the classification logic from `exercises_classifier.py` to the extracted text, creating a master CSV file of classified exercises (`TODOS_classified.csv`).

- **Data Curation and Exploration:**
    - `csv_explorer.ipynb`: A notebook for data cleaning, manual corrections, and splitting the main classified CSV into smaller, more specific CSV files. These final CSVs are stored in the `tipos_csv/` directory.
    - The `csv/` directory and its subdirectories store the intermediate and final CSV files generated throughout the process.

- **User Interface:**
    - `app.py`: A Streamlit web application that provides a user interface to view and filter the classified exercises. It reads the data from the CSV files in the `tipos_csv/` directory.

- **Database (secondary/incomplete):**
    - `tables_creation.sql` and `database.ipynb`: These files suggest an effort to create a MySQL database for storing the data, but this part of the project appears to be incomplete, with the primary workflow relying on CSV files.

In summary, your project successfully automates the classification of exercises from PDF files, with a clear pipeline from data acquisition to a user-friendly web interface.
