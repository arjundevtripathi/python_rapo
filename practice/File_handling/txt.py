# with open("student.txt","w") as file:
#     file.write("this is python")
#     print("File Created")


# with open("student.txt","r") as file:
#     print(file.read())
    
    

name = ["a","ab"]
for i in name:
    with open(f"{i}.txt","w") as file:
        file.write("this is python")
        print("File Created")

# delete file
import os

for i in name:
    os.remove(f"{i}.txt")
    print("File Deleted")