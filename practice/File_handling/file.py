# wap to create a file  emp_name = ["arjun","aman",akash,"kamal"] then write their name and Emp_id
# in the file and then read the file and print the data in the file. 



# emp_name = ["arjun", "aman", "akash", "kamal"]
# for i in emp_name:
#     with open(f"{i}.txt", "w") as file:
#         emp_id = input(f"Enter Emp_id for {i}: ")
#         emp_name = input(f"Enter Emp_name for {i}: ")
        
#         file.write(f"Emp Name: {emp_name}\nEmp ID: {emp_id}\n")
#         print(f"File Created: {i}.txt")

# for i in emp_name:
#     with open(f"{i}.txt", "r") as file:
#         print(file.read())
        




# delete file
# import os

# for i in emp_name:
#     os.remove(f"{i}.txt")
#     print(f"File Deleted: {i}.txt")








# import random
# import string

# employees = ["arjun", "aman", "akash", "kamal"]

# # Create employee files
# for employee in employees:
#     emp_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
#     emp_name = input(f"Enter Employee Name for {employee}: ")

#     with open(f"{employee}.txt", "w") as file:
#         file.write(f"Emp Name: {emp_name}\n")
#         file.write(f"Emp ID: {emp_id}\n")

#     print(f"{employee}.txt created successfully.")

# # Read employee files
# print("\nEmployee Details:\n")

# for employee in employees:
#     with open(f"{employee}.txt", "r") as file:
#         print(file.read())