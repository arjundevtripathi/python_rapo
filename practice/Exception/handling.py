# file = open("student.txt", "r")

# print("file Created")
# # print(file.read())
# file.close()


# with open("student.txt", "r") as file:
#     lines = file.readlines()
#     print(lines)


# with open("student.txt", "r") as file:
#     data = file.read()
#     print(data)



# with open("student.txt", "r") as file:
#     print(file.readline())



# with open("student.txt", "r") as file:
#     lines = file.readlines()
#     print(lines)


# with open("student.txt", "r") as file:
#     for line in file:
#         print(line.strip())
        
        
# with open("stu.txt", "w") as file:
#     # file.write("Python programming language")



# with open("stu.txt", "r") as file:
#     print(file.read())
    

# data = b"Hello"

# with open("binary.bin", "wb") as file:
#     file.write(data)


# with open("binary.bin", "rb") as file:
#     print(file.read())



# try:
#     with open("student.txt", "r") as file:
#         print(file.read())
# except FileNotFoundError:
#     print("File not found.")




import os
filename = "student.txt"

# CREATE
with open(filename, "w") as file:
    file.write("Arjun\n")
    file.write("Rahul\n")
    print("File Created")

# READ
with open(filename, "r") as file:
    print("File Content:")
    print(file.read())

# UPDATE (Append)
with open(filename, "a") as file:
    file.write("Ankit\n")
    file.write("Aman\n")

# READ AGAIN
with open(filename, "r") as file:
    print("\nUpdated Content:")
    print(file.read())

# DELETE
if os.path.exists(filename):
    os.remove(filename)
    print("\nFile deleted successfully.")