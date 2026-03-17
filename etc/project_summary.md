# emestrada_parser — Project Summary

## Overview

A full end-to-end pipeline to collect, parse, store, and classify Spanish university entrance exam (Selectividad/PAU) exercises from [emestrada.org](https://www.emestrada.org).

The pipeline covers three subjects: **Física**, **Química**, and **Matemáticas CCSS**, spanning exam years from 2000 to 2024.

---

## Pipeline Stages

### 1. Crawling — `jupyter notebooks/emestrada_crawler.ipynb`
Downloads PDF exam files from `emestrada.org/wp-content/uploads/`.
- Probes remote folders to find which year/month paths contain files.
- Caches discovered folder paths in `remote_folders.txt` to avoid redundant requests.
- Downloads PDFs organized locally by subject and topic (e.g. `Física/Campo gravitatorio/2022 - Campo gravitatorio.pdf`).

### 2. Parsing — `jupyter notebooks/pdf_parser.ipynb`
Converts PDFs to structured data using OCR.
- Converts PDF pages to images with `pdf2image`.
- Extracts text using `pytesseract` (Spanish language model).
- Parses each page into fields: `subject`, `year`, `topic`, `exam`, `exercise`, `statement`.
- Handles errors with a dated log file (`error_logs/errors_DD-MM-YYYY.log`).
- Sends Telegram bot notifications for long-running processing jobs.
- Outputs per-topic CSVs (e.g. `exercises_Equilibrio Químico.csv`) and a combined `TODOS.csv`.

### 3. Data Cleaning — `dataframes/fisica.ipynb`
Merges and normalizes all subject CSVs into a single `TODOS.csv`.
- Standardizes the `exercise` column (adds commas, fixes encoding artifacts like `Opcióon → Opción`, normalizes Roman numerals like `Il → II`, `Iil → III`).
- Combines Física, Mates CCSS, and Química into one unified dataframe (~3,294 rows).

### 4. CSV Exploration — `jupyter notebooks/csv_explorer.ipynb`
Ad-hoc data exploration and cleaning for the Mates CCSS subject.
- Inspects unique values per column across all topic CSVs.
- Fixes minor data entry errors (e.g. `'Tunto' → 'Junio'`).

### 5. Database Loading — `jupyter notebooks/database.ipynb`
Loads the cleaned data into a MySQL database.
- Reads connection credentials from `db_credentials.json`.
- Inserts unique values from `TODOS.csv` into lookup tables: `subjects`, `years`, `topics`, `exams`, `exercises`.

### 6. Keyword-based Classification — `jupyter notebooks/test_classifier.ipynb`
Classifies exercises by type using keyword matching.
- Reads topic-specific keyword dictionaries from JSON files (e.g. `keywords_quimica.json`).
- Assigns an `exercise_type` label per statement (e.g. `"Teoría de Brönsted-Lowry"`, `"Ajuste reacción redox"`).
- Falls back to `"{topic} varios"` when no keyword matches.
- Exports to `TODOS_classified.csv`.

### 7. AI Classification — `csv/QUIMICA/api pipeline.ipynb`
Classifies exercises using the Claude API (Anthropic).
- Uses `claude-haiku` model with topic-specific system prompts loaded from `.md` files.
- Sends exercise data as CSV text to the model and receives labeled rows back.
- Returns fine-grained exercise types (e.g. `"principio de LeChatelier"`, `"cálculo de las constantes Kc y Kp"`, `"ejercicios con resolución de ecuación de 2do grado"`).

---

## Data Schema

Each exercise record contains the following fields:

| Field | Description | Example |
|---|---|---|
| `subject` | Subject name | `Química`, `Física`, `Mates CCSS` |
| `year` | Exam year | `2018` |
| `topic` | Topic within the subject | `Equilibrio Químico` |
| `exam` | Exam session | `Junio`, `Reserva 1`, `Septiembre` |
| `exercise` | Exercise identifier | `Ejercicio 5, Opción B` |
| `statement` | Full exercise text (OCR) | `PCl3(g) ⇌ PCl2(g) + Cl2(g)...` |
| `exercise_type` | Classification label (optional) | `principio de LeChatelier` |

---

## Subjects and Topics

### Física
- Campo gravitatorio
- Campo electromagnético
- Movimiento ondulatorio
- Óptica geométrica
- Física cuántica y nuclear

### Química
- Equilibrio Químico
- Ácido Base
- Cantidad Química
- Configuración Electrónica
- Reacciones Redox
- Reactividad Orgánica
- Termoquímica
- Formulación
- Solubilidad
- Enlace Químico

### Matemáticas CCSS
- Matrices y Determinantes
- Sistemas de Ecuaciones Lineales
- Probabilidad
- Inferencia Estadística
- Contraste de Hipótesis
- Funciones CCSS
- Programación Lineal

---

## Key Files

| Path | Description |
|---|---|
| `csv/TODOS.csv` | Combined dataset (~3,294 exercises, all subjects) |
| `csv/TODOS_classified.csv` | Dataset with keyword-based `exercise_type` labels |
| `csv/FISICA/FISICA.csv` | Física exercises |
| `csv/QUIMICA/QUIMICA.csv` | Química exercises |
| `csv/MATES CCSS/MATES_CCSS.csv` | Mates CCSS exercises |
| `remote_folders.txt` | Cached list of remote folders with PDFs |
| `error_logs/` | OCR parsing error logs |
| `db_credentials.json` | MySQL connection credentials (not in repo) |

---

## Dependencies

- `pdf2image` + `poppler` — PDF to image conversion
- `pytesseract` + `tesseract-ocr-spa` — Spanish OCR
- `pandas`, `numpy` — Data manipulation
- `mysql-connector-python` — Database loading
- `anthropic` — Claude API for AI classification
- `requests` — Web crawling
- `python-dotenv` — Environment variable management
