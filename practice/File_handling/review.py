import mysql.connector

# review = [
#     {
#         "negative": "This is very bad product.It did not meet my expectations at all.",
#         "positive": "This product exceeded my expectations. I am very satisfied with my purchase.",
#         "bad_product": ["Shoes", "Shirt", "Pants"],
#         "good_product": ["Laptop", "Smartphone", "Headphones"]
#     }
# ]

# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="1234",
#     database="ecommerce"
# )

# cursor = conn.cursor()

# create_table = """
# CREATE TABLE IF NOT EXISTS PRODUCT_REVIEWS (
#     negative VARCHAR(255),
#     positive VARCHAR(255),
#     bad_product VARCHAR(255),
#     good_product VARCHAR(255)
# );
# """

# cursor.execute(create_table)

# sql = """
# INSERT INTO PRODUCT_REVIEWS
# (negative, positive, bad_product, good_product)
# VALUES (%s, %s, %s, %s)
# """

# for item in review:
#     values = (
#         item["negative"],
#         item["positive"],
#         ", ".join(item["bad_product"]),
#         ", ".join(item["good_product"])
#     )

#     cursor.execute(sql, values)

# conn.commit()

# cursor.close()
# conn.close()

# print("Data inserted successfully.")

# import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="ecommerce"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM PRODUCT_REVIEWS")

rows = cursor.fetchall()

with open("reviews.txt", "w", encoding="utf-8") as file:
    for row in rows:
        file.write(f"Negative: {row[0]}\n")
        file.write(f"Positive: {row[1]}\n")
        file.write(f"Bad Products: {row[2]}\n")
        file.write(f"Good Products: {row[3]}\n")
        file.write("-" * 50 + "\n")

cursor.close()
conn.close()

print("Data exported to reviews.txt")