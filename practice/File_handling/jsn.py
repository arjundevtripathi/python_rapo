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


# import json

# student = {}

# student["id"] = int(input("Enter ID: "))
# student["name"] = input("Enter Name: ")
# student["age"] = int(input("Enter Age: "))
# student["marks"] = float(input("Enter Marks: "))

# with open("student.json", "w") as file:
#     json.dump(student, file, indent=4)

# print("Student saved successfully!")



    


with open("product.json", "r") as file:
    r=file.read()
    print(type(r))
    
    
# convert string to dictionary
import json 

data = json.loads(r)
print(type(data))


# # now create a new txt file and write only value of id, title, description, category, price, discountPercentage in the new txt file.
# with open("product.txt", "w") as file:
#     file.write(f"id: {data['id']}\n")
#     file.write(f"title: {data['title']}\n")
#     file.write(f"description: {data['description']}\n")
#     file.write(f"category: {data['category']}\n")
#     file.write(f"price: {data['price']}\n")
#     file.write(f"discountPercentage: {data['discountPercentage']}\n")
#     file.write(f"rating: {data['rating']}\n")
#     file.write(f"stock: {data['stock']}\n")
#     file.write(f"tags: {data['tags']}\n")
    
  





  
  
import json
import mysql.connector

# Read JSON file
with open("product.json", "r") as file:
    data = json.load(file)

# Print JSON data
# print(data)

# Print all keys
# for key in data:
#     print(key)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",   # Replace with your password
    database="ecommerce"
)

cursor = conn.cursor()

# Create table if it doesn't exist
create_table = """
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY,
    title VARCHAR(200),
    description TEXT,
    category VARCHAR(100),
    price DECIMAL(10,2),
    discountPercentage FLOAT,
    rating FLOAT,
    stock INT,
    brand VARCHAR(100),
    sku VARCHAR(50),
    weight INT,
    warrantyInformation VARCHAR(100),
    shippingInformation VARCHAR(100),
    availabilityStatus VARCHAR(50),
    returnPolicy VARCHAR(100),
    minimumOrderQuantity INT,
    thumbnail TEXT
)
"""

cursor.execute(create_table)

# Insert query
sql = """
INSERT INTO products (
    id, title, description, category, price,
    discountPercentage, rating, stock, brand, sku,
    weight, warrantyInformation, shippingInformation,
    availabilityStatus, returnPolicy,
    minimumOrderQuantity, thumbnail
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

values = (
    data["id"],
    data["title"],
    data["description"],
    data["category"],
    data["price"],
    data["discountPercentage"],
    data["rating"],
    data["stock"],
    data["brand"],
    data["sku"],
    data["weight"],
    data["warrantyInformation"],
    data["shippingInformation"],
    data["availabilityStatus"],
    data["returnPolicy"],
    data["minimumOrderQuantity"],
    data["thumbnail"]
)

cursor.execute(sql, values)
conn.commit()

print("Data inserted successfully!")

# Close connection
cursor.close()
conn.close()