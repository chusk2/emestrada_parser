# MySQL and Python: Best Practices and Code Examples

## 🔹 Choosing the Best MySQL Connector for Python

### ✅ Recommended: `mysql-connector-python`
- Official MySQL library (developed by Oracle)
- No external dependencies
- Supports transactions and prepared statements

### 🛠 Installation
```bash
pip install mysql-connector-python
```

### 📌 Connecting to MySQL
```python
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="your_user",
    password="your_password",
    database="your_database"
)

cursor = conn.cursor()
print("Connected successfully")
```

---

## 🔹 Executing SQL Queries from Python

### **1️⃣ Creating Tables**
```sql
CREATE TABLE IF NOT EXISTS years (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT UNIQUE
);

CREATE TABLE IF NOT EXISTS subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS exercises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year_id INT,
    subject_id INT,
    FOREIGN KEY (year_id) REFERENCES years(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
);
```
```python
cursor.execute("CREATE TABLE IF NOT EXISTS years (id INT AUTO_INCREMENT PRIMARY KEY, year INT UNIQUE);")
cursor.execute("CREATE TABLE IF NOT EXISTS subjects (id INT AUTO_INCREMENT PRIMARY KEY, subject VARCHAR(255) UNIQUE);")
cursor.execute("CREATE TABLE IF NOT EXISTS exercises (id INT AUTO_INCREMENT PRIMARY KEY, year_id INT, subject_id INT, FOREIGN KEY (year_id) REFERENCES years(id), FOREIGN KEY (subject_id) REFERENCES subjects(id));")

conn.commit()
```

### **2️⃣ Inserting Data Using Pandas**
```python
import pandas as pd

df = pd.DataFrame({"year": [2023, 2024, 2025]})

for _, row in df.iterrows():
    cursor.execute("INSERT INTO years (year) VALUES (%s)", (row["year"],))

conn.commit()
print("Data inserted successfully")
```

### **🔥 Optimized Batch Insert**
```python
data = list(df["year"].unique())  
cursor.executemany("INSERT INTO years (year) VALUES (%s)", [(year,) for year in data])
conn.commit()
```

### **3️⃣ Closing the Connection**
```python
cursor.close()
conn.close()
```

---

## 🔹 Understanding Placeholders in SQL Queries

| Placeholder | Example | Used In | Best For |
|------------|---------|--------|-----------|
| `%s` | `"VALUES (%s, %s)"` | MySQL (`mysql-connector-python`, `pymysql`) | **MySQL queries** |
| `?` | `"VALUES (?, ?)"` | SQLite (`sqlite3`) | **SQLite databases** |
| `:named` | `"VALUES (:name, :age)"` | SQLite, SQLAlchemy | **Named parameters** (clearer) |
| `%(name)s` | `"VALUES (%(name)s, %(age)s)"` | MySQL | **Dictionary-based queries** |

**🚀 For MySQL, use `%s` for simple queries and `%(name)s` for dictionary-based queries.**

---

## 🔹 Summary

- `mysql-connector-python` is the **simplest and most recommended** MySQL connector.
- Using **parameterized queries (`%s`)** is the **safest** way to execute SQL queries.
- **Batch inserts** (`executemany()`) are **faster** than inserting row by row.
- **Different placeholders** exist depending on the database driver.

🚀 **For most MySQL projects, using `mysql-connector-python` with `%s` placeholders is the best approach!**
