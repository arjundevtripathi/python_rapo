# 1. create a empty list and add 5 elements to it using append() method
# my_list = []
# my_list.append(1)
# my_list.append(2)   
# my_list.append(3)
# print(my_list)


# 2. create a empty list and add 5 elements to it using input() method
lis = []
print("Enter 5 elements to add to the list:")
for i in range(5):
    element = input(f"Element {i+1}: ")
    lis.append(element)

print("List with user-provided elements:", lis)


