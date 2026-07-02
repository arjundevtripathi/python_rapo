import json
import mysql.connector

# ----------------------------------------------------------------------
# Helper: load JSON from a file
# ----------------------------------------------------------------------
def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# ----------------------------------------------------------------------
# Database operations
# ----------------------------------------------------------------------
def create_database(cursor, db_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    print(f"Database '{db_name}' created successfully (or already exists).")

def use_database(cursor, db_name):
    cursor.execute(f"USE {db_name}")
    print(f"Using database '{db_name}'.")

def create_table(cursor, table_name, columns_def):
    col_definitions = [f"{col} {dtype}" for col, dtype in columns_def.items()]
    query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(col_definitions)})"
    cursor.execute(query)
    print(f"Table '{table_name}' created successfully.")

def insert_data(cursor, table_name, columns, data_rows):
    column_names = list(columns.keys())
    placeholders = ', '.join(['%s'] * len(column_names))
    query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"
    
    for row in data_rows:
        # Build a lowercase-key version of the row for case‑insensitive lookup
        row_lower = {k.lower(): v for k, v in row.items()}
        values = tuple(row_lower[col.lower()] for col in column_names)
        cursor.execute(query, values)
    
    print(f"{len(data_rows)} rows inserted successfully.")

# ----------------------------------------------------------------------
# Main workflow
# ----------------------------------------------------------------------
def main():
    # 1. Load schema and data from JSON files
    schema = load_json("student.json")
    data = load_json("students.json")

    # 2. Extract configuration
    db_name = schema['database']
    table_name = schema['table_name']
    columns_def = schema['columns']          # e.g. {"id": "INT", "name": "VARCHAR(100)"}
    student_data = data["student"]           # list of dictionaries

    # 3. Connect to MySQL (no database selected yet)
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234"
    )
    cursor = conn.cursor()

    try:
        # 4. Create and use database
        create_database(cursor, db_name)
        use_database(cursor, db_name)

        # 5. Create table
        create_table(cursor, table_name, columns_def)

        # 6. Insert all rows
        insert_data(cursor, table_name, columns_def, student_data)

        conn.commit()
        print("All operations completed successfully.")

    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()