import os
import pymysql
import json
from dotenv import load_dotenv

load_dotenv()

# Get database name from .env or schema.json
DB_NAME = os.getenv('DB_NAME')

def db_connect():
    conn = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=int(os.getenv('DB_PORT', 3306))
    )
    return conn

def db_creation():
    conn = db_connect()
    cur = conn.cursor()
    
    # Use DB_NAME from .env if available, otherwise from schema.json
    with open("database/schema.json", "r") as f:
        schema_data = json.load(f)
    
    # Use .env DB_NAME first, fallback to schema.json
    database_name = DB_NAME if DB_NAME else schema_data['database']
    
    try:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"✅ Database '{database_name}' created successfully.")
        conn.commit()
    except Exception as e:
        print(f"❌ Error creating database: {e}")
    finally:
        cur.close()
        conn.close()
    
    return database_name

def create_table():
    # Load schema
    with open("database/schema.json", "r") as f:
        data = json.load(f)
    
    # Use DB_NAME from .env if available
    database_name = DB_NAME if DB_NAME else data['database']
    
    table = data['table']
    cols = ", ".join([f"{col} {dcol}" for col, dcol in data['columns'].items()])
    print(f"📋 Columns: {cols}")
    
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute(f"USE {database_name}")
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table} ({cols})")
        print(f"✅ Table '{table}' created successfully in database '{database_name}'.")
        conn.commit()
    except Exception as e:
        print(f"❌ Error creating table: {e}")
    finally:
        cur.close()
        conn.close()

def verify_table():
    conn = db_connect()
    cur = conn.cursor()
    with open("database/schema.json", "r") as f:
        data = json.load(f)
    
    database_name = DB_NAME if DB_NAME else data['database']
    table = data['table']
    
    try:
        cur.execute(f"USE {database_name}")
        cur.execute(f"DESCRIBE {table}")
        results = cur.fetchall()
        print(f"\n✅ Table '{table}' structure verified:")
        for row in results:
            print(f"  {row[0]} - {row[1]}")
    except Exception as e:
        print(f"❌ Error verifying table: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    print("🚀 Starting database initialization...")
    db_creation()
    create_table()
    verify_table()
    print("\n✅ Done!")