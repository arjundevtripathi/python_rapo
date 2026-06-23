# # 1. Sum of all elements
# lst = [10, 20, 30, 40, 50]
# print("Sum:", sum(lst))

    

# str1 = [22,25,24,26,30]
# new_list = []
# for x in str1:
#     if x % 2 == 0:
#         new_list.append(f"{x} is even")
#     else:
#         new_list.append(f"{x} is odd")
# print("Results:", new_list)



# str2 = ["Hello", "World!"] 
# for i in range(len(str2)):
#     str2[i] = str2[i][::-1]
#     print("Reversed string:", str2[i])
    


# str2 = ["Hello", "World!"] 
# str2.reverse()
# print("Reversed string:", str2)



# wap to swap p from python and last g from programming  first and last element of a list
# like this ["Python Programming"] to ["gython ProgramminP"]

str3 = ["Python Programming"]
first_element = str3[0][0]  # Get the first character 'P'
last_element = str3[0][-1]  # Get the last character 'g'

first_element , last_element = last_element , first_element
print("Swapped string:", str3)
