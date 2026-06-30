import os

FILE = "students.txt"

def add_student():
    roll = input("Roll No: ")
    name = input("Name: ")
    marks = input("Marks: ")

    with open(FILE, "a") as f:
        f.write(f"{roll},{name},{marks}\n")

def view_students():
    if not os.path.exists(FILE):
        print("No records found")
        return

    with open(FILE, "r") as f:
        print("\nStudents")
        print("-"*30)
        for line in f:
            print(line.strip())

def search_student():
    roll = input("Enter Roll No: ")

    with open(FILE, "r") as f:
        for line in f:
            if line.startswith(roll + ","):
                print("Found:", line)
                return
    print("Not Found")

def update_student():
    roll = input("Roll No to Update: ")

    lines = []

    with open(FILE, "r") as f:
        for line in f:
            data = line.strip().split(",")

            if data[0] == roll:
                name = input("New Name: ")
                marks = input("New Marks: ")
                lines.append(f"{roll},{name},{marks}\n")
            else:
                lines.append(line)

    with open(FILE, "w") as f:
        f.writelines(lines)

def delete_student():
    roll = input("Roll No to Delete: ")

    lines = []

    with open(FILE, "r") as f:
        for line in f:
            if not line.startswith(roll + ","):
                lines.append(line)

    with open(FILE, "w") as f:
        f.writelines(lines)

while True:
    print("""
Select your choice:
1 Add
2 View
3 Search
4 Update
5 Delete
6 Exit
""")

    ch = input("Choice: ")

    if ch == "1":
        add_student()
    elif ch == "2":
        view_students()
    elif ch == "3":
        search_student()
    elif ch == "4":
        update_student()
    elif ch == "5":
        delete_student()
    elif ch == "6":
        break