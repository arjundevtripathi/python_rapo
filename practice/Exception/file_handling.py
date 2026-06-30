# what is file.
# file is collection of data which can be store on local device or on server.

# Types of file
# Text file.
# Binary (media)


# Path
# Relative (current working dir)
# Absolute (root dir)

# method and techniques to work with file.
# open('file_name',"mode",optional): to poen read and write the file.

# modes:
# x : strict for creating file.
# w : write to file
# r : read to file
# a : append or update to file
# w+ : read and write
# r+ : read and write
# a+ :update and read


# write() : use to write string data in file.
# writelines() : use to write collection(list, tuple, set) data in file.
# read()
# readlines()
# seek() : use to point the cursor.
# close() : use to close file.
# context manager : use to automatically close file without any buffer.



# create a file in write mode(w).
# file=open("demo.txt",'w')
# file.write("this is my new file by using contex manager")
# file.close()
# print("file created..")


# with open ("demo.txt","w") as file:
#     file.write("this is my new file by using contex manager")
#     print("file added done")
    
    
    

# try:
#     with open("demo.txt","w")as file:
#         file.write("this is my new file by using contex manager")
#         print("File added done")
# except Exception as e:
#     print(e)
    
    

# api="this is data from api"
# try:
#     with open("demo1.txt","w+") as file:
#         file.write(api)
#         file.seek(0)
#         r=file.read()
#         print(r)
# except Exception in e:
#     print(e)
    
    
    
    
# api=""" 
# Name : Arjun,
# Age :22,
# add : Noida
# """
# try:
#     with open("arjun2.txt","w+") as file:
#         file.write(api)
#         file.write("-"*20)
#         file.seek(0)
#         r=file.read()
#         print(r)
        
# except Exception in e:
#     print(e)
    
    
    
    
for i in range(3):
    with open("textt.txt", "a") as f:
        name = input("Enter your name: ")
        age = input("Enter your age: ")
        address = input("Enter your address: ")
        mobile = input("Enter your mobile number: ")

        f.write(f"Name    : {name}\n")
        f.write(f"Age     : {age}\n")
        f.write(f"Address : {address}\n")
        f.write(f"Mobile  : {mobile}\n")
        f.write("-" * 40 + "\n")  # Just to separate entries

print("Data added...")
