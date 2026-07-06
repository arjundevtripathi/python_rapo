import os
import pymysql
from dotenv import load_dotenv
import streamlit as st
import pandas as pd

load_dotenv()

DB_NAME = os.getenv('DB_NAME')

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': DB_NAME,
    'port': int(os.getenv('DB_PORT', 3306)),
    'cursorclass': pymysql.cursors.DictCursor,
}

print(f"DB_NAME: {DB_NAME}")

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

def insert_student(name, age, stu_reg_no):
    """Insert a new student into the database"""
    connection = get_connection()
    if connection is None:
        return False, "Database connection failed"
    
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO all_student (name, age, stu_reg_no) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, age, stu_reg_no))
            connection.commit()
            return True, f"Student '{name}' inserted successfully! ✅"
    except pymysql.MySQLError as e:
        return False, f"Error inserting student: {e}"
    finally:
        if connection:
            connection.close()

def get_all_students():
    """Get all students from the database"""
    connection = get_connection()
    if connection is None:
        return []
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM all_student ORDER BY id DESC")
            results = cursor.fetchall()
            return results
    except pymysql.MySQLError as e:
        print(f"Error fetching students: {e}")
        return []
    finally:
        if connection:
            connection.close()

# Streamlit UI
st.set_page_config(page_title="Student Management System", page_icon="🎓", layout="wide")

st.title("🎓 Student Management System")

# Check database health
health = check_health()
if health["status"] == "healthy":
    st.success(health["message"])
else:
    st.error(health["message"])
    st.stop()

# Main layout with two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Add New Student")
    with st.form("add_student_form"):
        name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=1, max_value=100, step=1)
        stu_reg_no = st.text_input("Registration Number")
        
        submitted = st.form_submit_button("Add Student", type="primary")
        
        if submitted:
            if not name or not stu_reg_no:
                st.error("Please fill in all fields")
            else:
                success, message = insert_student(name, age, stu_reg_no)
                if success:
                    st.success(message)
                    st.balloons()
                    st.rerun()
                else:
                    st.error(message)

with col2:
    st.subheader("📋 All Students")
    students = get_all_students()
    
    if students:
        df = pd.DataFrame(students)
        st.dataframe(df, use_container_width=True)
        st.info(f"Total Students: {len(students)}")
    else:
        st.info("No students found in the database")