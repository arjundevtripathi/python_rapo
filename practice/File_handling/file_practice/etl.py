import json
import mysql.connector
import csv
import logging
from mysql.connector import Error

# ----- CONFIG (edit these) -----
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '1234'
DB_NAME = 'student_db'
SCHEMA_FILE = 'student_schema.json'
DATA_FILE = 'students.json'
LOG_FILE = 'logs.txt'
EXPORT_FILE = 'exported_students.csv'
UNIQUE_KEY = 'student_id'   # used to detect duplicates

# ----- SIMPLE LOGGING -----
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def log(msg):
    print(msg)
    logging.info(msg)

# ----- CONNECT TO MYSQL (no separate function) -----
try:
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    log("Connected to MySQL.")
except Error as e:
    log(f"Connection failed: {e}")
    exit()

# ----- CREATE DATABASE & TABLE -----
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
cursor.execute(f"USE {DB_NAME}")

# Load schema from JSON
with open(SCHEMA_FILE) as f:
    schema = json.load(f)

table_name = schema['table_name']
columns = schema['columns']   # dict: {col: datatype}
col_names = list(columns.keys())

# Build CREATE TABLE
col_defs = [f"{col} {dtype}" for col, dtype in columns.items()]
cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(col_defs)})")
log(f"Table '{table_name}' ready.")

# ----- ETL: LOAD & TRANSFORM & INSERT/UPDATE -----
with open(DATA_FILE) as f:
    data = json.load(f)

inserted = updated = 0

for record in data.get('student', []):
    # Transform: extract values in correct order, convert age to int
    values = []
    for col in col_names:
        val = record.get(col.lower())
        if col == 'age' and val is not None:
            try:
                val = int(val)
            except:
                val = None
        values.append(val)

    # Get unique key value
    idx = col_names.index(UNIQUE_KEY)
    unique_val = values[idx]

    # Check if exists
    cursor.execute(f"SELECT 1 FROM {table_name} WHERE {UNIQUE_KEY} = %s", (unique_val,))
    exists = cursor.fetchone() is not None

    if exists:
        # UPDATE
        set_clause = ', '.join([f"{col} = %s" for col in col_names])
        cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {UNIQUE_KEY} = %s",
                       values + [unique_val])
        updated += 1
        log(f"Updated {UNIQUE_KEY}={unique_val}")
    else:
        # INSERT
        placeholders = ', '.join(['%s'] * len(col_names))
        cursor.execute(f"INSERT INTO {table_name} ({', '.join(col_names)}) VALUES ({placeholders})",
                       values)
        inserted += 1
        log(f"Inserted {UNIQUE_KEY}={unique_val}")

conn.commit()
log(f"ETL done: {inserted} inserted, {updated} updated.")

# ----- EXPORT TO CSV -----
cursor.execute(f"SELECT * FROM {table_name}")
rows = cursor.fetchall()
if rows:
    with open(EXPORT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([desc[0] for desc in cursor.description])
        writer.writerows(rows)
    log(f"Exported {len(rows)} rows to {EXPORT_FILE}")

# ----- CRUD MENU (direct, no extra functions) -----
while True:
    print("\n" + "="*40)
    print("  STUDENT CRUD (MySQL)")
    print("="*40)
    print("1. Add")
    print("2. View")
    print("3. Search by ID")
    print("4. Update")
    print("5. Delete")
    print("6. Exit")
    choice = input("Choice: ")

    if choice == '1':
        # Add
        values = []
        for col in col_names:
            val = input(f"{col}: ")
            if col == 'age':
                try:
                    val = int(val) if val.strip() else None
                except:
                    val = None
            values.append(val)
        try:
            placeholders = ', '.join(['%s'] * len(col_names))
            cursor.execute(f"INSERT INTO {table_name} ({', '.join(col_names)}) VALUES ({placeholders})",
                           values)
            conn.commit()
            log("Added student.")
            print("Added.")
        except Error as e:
            print("Error:", e)

    elif choice == '2':
        # View
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        if not rows:
            print("No records.")
        else:
            print(" | ".join(col_names))
            print("-"*50)
            for row in rows:
                print(" | ".join(str(x) for x in row))

    elif choice == '3':
        # Search
        val = input(f"Enter {UNIQUE_KEY}: ")
        cursor.execute(f"SELECT * FROM {table_name} WHERE {UNIQUE_KEY} = %s", (val,))
        row = cursor.fetchone()
        if row:
            print(" | ".join(str(x) for x in row))
        else:
            print("Not found.")

    elif choice == '4':
        # Update
        uid = input(f"Enter {UNIQUE_KEY} to update: ")
        cursor.execute(f"SELECT * FROM {table_name} WHERE {UNIQUE_KEY} = %s", (uid,))
        row = cursor.fetchone()
        if not row:
            print("Not found.")
            continue
        print("Leave blank to keep current value.")
        new_vals = []
        for i, col in enumerate(col_names):
            current = row[i]
            new_val = input(f"{col} (current: {current}): ")
            if new_val.strip() == "":
                new_val = current
            elif col == 'age':
                try:
                    new_val = int(new_val)
                except:
                    new_val = current
            new_vals.append(new_val)
        set_clause = ', '.join([f"{col} = %s" for col in col_names])
        cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {UNIQUE_KEY} = %s",
                       new_vals + [uid])
        conn.commit()
        log(f"Updated {UNIQUE_KEY}={uid}")
        print("Updated.")

    elif choice == '5':
        # Delete
        uid = input(f"Enter {UNIQUE_KEY} to delete: ")
        cursor.execute(f"DELETE FROM {table_name} WHERE {UNIQUE_KEY} = %s", (uid,))
        conn.commit()
        if cursor.rowcount:
            log(f"Deleted {UNIQUE_KEY}={uid}")
            print("Deleted.")
        else:
            print("Not found.")

    elif choice == '6':
        break

# Cleanup
cursor.close()
conn.close()
log("Goodbye.")