import streamlit as st
import pandas as pd
import json
import mysql.connector
import csv
import logging
import os
from mysql.connector import Error

# ---------- CONFIG ----------
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '1234'
DB_NAME = 'student_db'
SCHEMA_FILE = 'student_schema.json'
DATA_FILE = 'students.json'
LOG_FILE = 'logs.txt'
EXPORT_FILE = 'exported_students.csv'
UNIQUE_KEY = 'student_id'

# ---------- DEFAULT SCHEMA ----------
DEFAULT_SCHEMA = {
    "database": DB_NAME,
    "table_name": "students",
    "columns": {
        "student_id": "INT PRIMARY KEY",
        "first_name": "VARCHAR(50)",
        "last_name": "VARCHAR(50)",
        "age": "INT",
        "grade": "VARCHAR(10)"
    }
}

# ---------- DEFAULT DATA (with student_id for all) ----------
DEFAULT_DATA = {
    "student": [
        {"student_id": 1, "first_name": "John", "last_name": "Doe", "age": 20, "grade": "A"},
        {"student_id": 2, "first_name": "Jane", "last_name": "Smith", "age": 22, "grade": "B"},
        {"student_id": 3, "first_name": "Alice", "last_name": "Johnson", "age": 21, "grade": "A-"}
    ]
}

# ---------- LOGGING ----------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)

def log(msg):
    logging.info(msg)

# ---------- LOAD SCHEMA (file or default) ----------
def load_schema():
    if os.path.exists(SCHEMA_FILE):
        with open(SCHEMA_FILE) as f:
            return json.load(f)
    else:
        with open(SCHEMA_FILE, 'w') as f:
            json.dump(DEFAULT_SCHEMA, f, indent=4)
        st.info("📄 Created default schema file: student_schema.json")
        return DEFAULT_SCHEMA

# ---------- LOAD DATA (file or default) ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    else:
        with open(DATA_FILE, 'w') as f:
            json.dump(DEFAULT_DATA, f, indent=4)
        st.info("📄 Created default data file: students.json")
        return DEFAULT_DATA

# ---------- DATABASE CONNECTION ----------
def get_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Error as e:
        st.error(f"❌ Database connection failed: {e}")
        return None

def ensure_db_and_table(schema):
    conn = get_connection()
    if not conn:
        return None, None
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        table_name = schema['table_name']
        columns = schema['columns']
        col_defs = [f"{col} {dtype}" for col, dtype in columns.items()]
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(col_defs)})")
        conn.commit()
        return conn, cursor
    except Error as e:
        st.error(f"❌ Database error: {e}")
        conn.close()
        return None, None

# ---------- LOAD DATA FROM DB (cached) ----------
@st.cache_data(ttl=60)
def load_data_from_db(schema):
    conn, cursor = ensure_db_and_table(schema)
    if not conn:
        return pd.DataFrame()
    try:
        table_name = schema['table_name']
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=col_names)
        return df
    except Error as e:
        st.error(f"❌ Failed to load data: {e}")
        return pd.DataFrame()
    finally:
        cursor.close()
        conn.close()

# ---------- ETL FUNCTION (FIXED) ----------
def run_etl(schema):
    data = load_data()
    records = data.get('student', [])
    if not records:
        return "No student records found in students.json."

    conn, cursor = ensure_db_and_table(schema)
    if not conn:
        return "Database connection failed."

    table_name = schema['table_name']
    columns = schema['columns']
    col_names = list(columns.keys())

    inserted = updated = skipped = 0

    for record in records:
        # Ensure unique key exists; if not, skip this record
        if UNIQUE_KEY not in record or record[UNIQUE_KEY] is None:
            skipped += 1
            log(f"Skipped record missing {UNIQUE_KEY}: {record}")
            continue

        # Build values in correct column order
        values = []
        for col in col_names:
            val = record.get(col.lower())  # case-insensitive
            if col == 'age' and val is not None:
                try:
                    val = int(val)
                except (ValueError, TypeError):
                    val = None
            values.append(val)

        # Extract unique value
        idx = col_names.index(UNIQUE_KEY)
        unique_val = values[idx]
        if unique_val is None:
            skipped += 1
            log(f"Skipped record with null {UNIQUE_KEY}: {record}")
            continue

        # Check existence
        cursor.execute(f"SELECT 1 FROM {table_name} WHERE {UNIQUE_KEY} = %s", (unique_val,))
        exists = cursor.fetchone() is not None

        if exists:
            set_clause = ', '.join([f"{col} = %s" for col in col_names])
            cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {UNIQUE_KEY} = %s",
                           values + [unique_val])
            updated += 1
            log(f"Updated {UNIQUE_KEY}={unique_val}")
        else:
            placeholders = ', '.join(['%s'] * len(col_names))
            cursor.execute(f"INSERT INTO {table_name} ({', '.join(col_names)}) VALUES ({placeholders})",
                           values)
            inserted += 1
            log(f"Inserted {UNIQUE_KEY}={unique_val}")

    conn.commit()
    cursor.close()
    conn.close()
    st.cache_data.clear()
    return f"✅ ETL completed: {inserted} inserted, {updated} updated, {skipped} skipped (missing {UNIQUE_KEY})."

# ---------- CRUD OPERATIONS ----------
def add_student(values, schema):
    conn, cursor = ensure_db_and_table(schema)
    if not conn:
        return False, "DB error"
    table_name = schema['table_name']
    col_names = list(schema['columns'].keys())
    placeholders = ', '.join(['%s'] * len(col_names))
    try:
        cursor.execute(f"INSERT INTO {table_name} ({', '.join(col_names)}) VALUES ({placeholders})", values)
        conn.commit()
        cursor.close()
        conn.close()
        st.cache_data.clear()
        return True, "Student added successfully."
    except Error as e:
        return False, f"Error: {e}"

def update_student(uid, new_values, schema):
    conn, cursor = ensure_db_and_table(schema)
    if not conn:
        return False, "DB error"
    table_name = schema['table_name']
    col_names = list(schema['columns'].keys())
    set_clause = ', '.join([f"{col} = %s" for col in col_names])
    try:
        cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {UNIQUE_KEY} = %s", new_values + [uid])
        conn.commit()
        cursor.close()
        conn.close()
        st.cache_data.clear()
        return True, "Student updated."
    except Error as e:
        return False, f"Error: {e}"

def delete_student(uid, schema):
    conn, cursor = ensure_db_and_table(schema)
    if not conn:
        return False, "DB error"
    table_name = schema['table_name']
    try:
        cursor.execute(f"DELETE FROM {table_name} WHERE {UNIQUE_KEY} = %s", (uid,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        st.cache_data.clear()
        if affected:
            return True, f"Deleted student with {UNIQUE_KEY}={uid}."
        else:
            return False, "Student not found."
    except Error as e:
        return False, f"Error: {e}"

def export_csv(schema):
    df = load_data_from_db(schema)
    if df.empty:
        return None
    return df.to_csv(index=False)

# ---------- STREAMLIT APP ----------
st.set_page_config(page_title="Student ETL + CRUD", layout="wide")
st.title("📘 Student Management System")
st.markdown("### ETL Pipeline + CRUD Operations with MySQL")

# Load schema (default if missing)
schema = load_schema()
col_names = list(schema['columns'].keys())

# Sidebar navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Choose an action", [
    "🏠 Dashboard", "⚙️ Run ETL", "📋 View Data",
    "➕ Add Student", "✏️ Update Student", "❌ Delete Student", "📥 Export CSV"
])

# Main content area
if option == "🏠 Dashboard":
    st.header("Dashboard")
    df = load_data_from_db(schema)
    if not df.empty:
        total = len(df)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Students", total)
        if 'grade' in df.columns:
            grade_counts = df['grade'].value_counts()
            if not grade_counts.empty:
                col2.metric("Most Common Grade", grade_counts.idxmax())
        col3.metric("Last Updated", "Just now")
        st.subheader("Latest Students")
        st.dataframe(df.tail(5), use_container_width=True)
    else:
        st.info("📭 No data yet. Run ETL or add students.")

elif option == "⚙️ Run ETL":
    st.header("Run ETL Pipeline")
    if st.button("🚀 Execute ETL", type="primary"):
        with st.spinner("Running ETL..."):
            result = run_etl(schema)
            st.success(result)
            if "completed" in result:
                st.balloons()
    st.info("This will load data from students.json, transform, and insert/update into MySQL.")

elif option == "📋 View Data":
    st.header("All Student Records")
    df = load_data_from_db(schema)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No records found.")

elif option == "➕ Add Student":
    st.header("Add New Student")
    with st.form("add_form"):
        values = []
        cols = st.columns(len(col_names))
        for i, col in enumerate(col_names):
            with cols[i]:
                if col == 'age':
                    val = st.number_input(col, min_value=0, step=1, key=f"add_{col}")
                else:
                    val = st.text_input(col, key=f"add_{col}")
                values.append(val)
        submitted = st.form_submit_button("Add Student")
        if submitted:
            if 'age' in col_names:
                idx = col_names.index('age')
                values[idx] = int(values[idx]) if values[idx] else None
            success, msg = add_student(values, schema)
            if success:
                st.success(msg)
                st.balloons()
            else:
                st.error(msg)

elif option == "✏️ Update Student":
    st.header("Update Student")
    uid_input = st.text_input(f"Enter {UNIQUE_KEY} of student to update")
    if uid_input:
        try:
            uid = int(uid_input)
        except ValueError:
            uid = uid_input
        df = load_data_from_db(schema)
        if df.empty:
            st.warning("No data in database.")
        else:
            row = df[df[UNIQUE_KEY] == uid]
            if row.empty:
                st.warning("Student not found.")
            else:
                with st.form("update_form"):
                    new_vals = []
                    cols = st.columns(len(col_names))
                    for i, col in enumerate(col_names):
                        current = row.iloc[0][col]
                        with cols[i]:
                            if col == 'age':
                                val = st.number_input(col, value=int(current) if current else 0, step=1, key=f"upd_{col}")
                            else:
                                val = st.text_input(col, value=str(current) if current else "", key=f"upd_{col}")
                            new_vals.append(val)
                    submitted = st.form_submit_button("Update Student")
                    if submitted:
                        if 'age' in col_names:
                            idx = col_names.index('age')
                            new_vals[idx] = int(new_vals[idx]) if new_vals[idx] else None
                        success, msg = update_student(uid, new_vals, schema)
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)

elif option == "❌ Delete Student":
    st.header("Delete Student")
    uid_input = st.text_input(f"Enter {UNIQUE_KEY} to delete")
    if st.button("Delete", type="primary"):
        if uid_input:
            try:
                uid = int(uid_input)
            except ValueError:
                uid = uid_input
            success, msg = delete_student(uid, schema)
            if success:
                st.success(msg)
            else:
                st.error(msg)
        else:
            st.warning("Please enter an ID.")

elif option == "📥 Export CSV":
    st.header("Export Data as CSV")
    csv_data = export_csv(schema)
    if csv_data is None:
        st.warning("No data to export.")
    else:
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=EXPORT_FILE,
            mime="text/csv",
        )
        st.success("Ready to download.")

# Show logs
with st.expander("📜 View Logs (logs.txt)"):
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            st.text(f.read())
    else:
        st.info("No logs yet.")