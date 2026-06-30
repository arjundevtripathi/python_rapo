# import json

# employees=[
#     {
#         "id":101,
#         "name":"Arjun",
#         "salary":80000
#     },
#     {
#         "id":102,
#         "name":"Rahul",
#         "salary":90000
#     }
# ]

# with open("employee1.json","w") as f:
#     json.dump(employees,f,indent=4)

# with open("employee.json") as f:
#     data=json.load(f)

# for emp in data:
#     print(emp)
    
    
    
# 


# import json

# students = [
#     {
#         "id": 101,
#         "name": "Arjun",
#         "marks": 90
#     },
#     {
#         "id": 102,
#         "name": "Rahul",
#         "marks": 85
#     },
#     {
#         "id": 103,
#         "name": "Amit",
#         "marks": 88
#     }
# ]

# with open("students.json", "w") as file:
#     json.dump(students, file, indent=4)

# print("students.json created successfully!")


# import json

# employee = {
#     "id": 1001,
#     "name": "Arjun",
#     "department": "Data Science",
#     "salary": 95000,
#     "skills": [
#         "Python",
#         "SQL",
#         "Machine Learning"
#     ],
#     "address": {
#         "city": "Bangalore",
#         "state": "Karnataka",
#         "country": "India"
#     }
# }

# with open("employee.json", "w") as file:
#     json.dump(employee, file, indent=4)
#     print("Flie Created")


import json

student = {}

student["id"] = int(input("Enter ID: "))
student["name"] = input("Enter Name: ")
student["age"] = int(input("Enter Age: "))
student["marks"] = float(input("Enter Marks: "))

with open("student.json", "w") as file:
    json.dump(student, file, indent=4)

print("Student saved successfully!")