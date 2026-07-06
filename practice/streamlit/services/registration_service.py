from config.config import get_connection

def insert_student(name, age, stu_reg_no):
    connection = get_connection()
    if connection is None:
        print("Error connecting to the database.")
        return None
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO all_student (name, age, stu_reg_no)
                VALUES (%s, %s, %s)
            """, (name, age, stu_reg_no))

        connection.commit()

    except Exception as e:
        connection.rollback()
        return False, str(e)

    finally:
        connection.close()