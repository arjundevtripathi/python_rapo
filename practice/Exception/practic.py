import os
# print(os.listdir())

print("Current Folder", os.getcwd())



emp_list = ["aman", "shivam", "ram", "kamal"]

for i in emp_list:
    os.remove(f"{i}.txt")
    print(i, "removed")
    

# emp_list = ["aman", "shivam", "ram", "kamal"]
# for i in emp_list:
#     with open(f"{i}.txt", "w") as file:
#         print(f"File Created: {i}.txt")


