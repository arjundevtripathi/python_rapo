import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': DB_NAME,
    'port': int(os.getenv('DB_PORT',3306)),
    'cursorclass': pymysql.cursors.DictCursor,
}

print("DB_NAME:", os.getenv('DB_NAME'))
def get_connection():
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to the database: {e}")
        return None
    

def check_health():
    connection = get_connection()
    if connection is None:
        return {"status": "unhealthy", "message": "Unable to connect to the database. ❌"}
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                return {"status": "healthy", "message": "Database connection is healthy. ✅"}
            else:
                return {"status": "unhealthy", "message": "Database connection is unhealthy. ❌"}
    except pymysql.MySQLError as e:
        return {"status": "unhealthy", "message": str(e)}
    
    finally:
        if connection:
            connection.close()