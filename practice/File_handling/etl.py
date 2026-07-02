# import pymysql
import json
import mysql.connector

with open("student.json", "r") as f:
    schema = json.load(f)
    
    
with open("students.json", "r") as f:
    data = json.load(f)
    
# DB connection   
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234"
)

cursor = conn.cursor()

# DATABASE CREATION
db_name = schema['database']
print(f"Database Name: {db_name}")

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
print(f"Database '{db_name}' created successfully.")

cursor.execute(f"USE {db_name}")
print(f"Using database '{db_name}'.")

# TABLE CREATION
col_definitions = [f"{col} {dtype}" for col, dtype in schema['columns'].items()]
# print(f"Column Definitions: {col_definitions}")
create_table_query = f"CREATE TABLE IF NOT EXISTS {schema['table_name']} ({', '.join(col_definitions)})"
cursor.execute(create_table_query)
print(f"Table '{schema['table_name']}' created successfully.")

# DATA INSERTION
insert_query = f"INSERT INTO {schema['table_name']} ({', '.join(schema['columns'].keys())}) VALUES ({', '.join(['%s'] * len(schema['columns']))})"

for row in data["student"]:
    values = tuple(row[col.lower()] for col in schema['columns'].keys())
    cursor.execute(insert_query, values)

conn.commit()
print("Data inserted successfully.")

cursor.close()
conn.close()
