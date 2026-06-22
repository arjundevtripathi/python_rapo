# wap to remove last word from the string
# str1 = "This is python code in VS"
# for i in range(len(str1)-1, -1, -1):
#     if str1[i] == ' ':
#         str1 = str1[:i]  # Remove the last word
#         break
    
# print(str1)


# wap to remove all words in which vowels are present
# str1 = "This is python code in VS"
# vowels = "aeiouAEIOU"
# words = str1.split()
# filtered_words = [word for word in words if not any(char in vowels for char in word)]
# str1 = " ".join(filtered_words)
# print(str1)



# str1 = "This is python code in VS"
# for i in range(len(str1)-1,):
#     if str1[i] == ' ':
#         str1 = str1[:i]  # Remove the last word
#         break

# print(str1)



# wap to count total whitespaces in the string
# str1 = "This is python code in VS" 
# count = 0
# for char in str1:
#     if char.isspace():
#         count += 1
# print("Total whitespaces:", count)



# # write a function to extract digits from the string
# str1 = "This is python code123 in VS version 35 address noida -11096"
# def extract_digits(input_string): 
#     digits = ''.join(char for char in input_string if char.isdigit())
#     return digits
# result = extract_digits(str1)
# print("Extracted digits:", result)  




# # write a function to remove all whitespaces from the string
# def remove_whitespaces(input_string):
#     return ''.join(input_string.split())
# str1 = "This is python code in VS"
# result = remove_whitespaces(str1)   
# print("String after removing whitespaces:", result)


# write a function to count total special characters in the string

def count_special_characters(input_string):
    count = 0
    for char in input_string:
        if not char.isalnum():
            count += 1
    return count

str1 = "This is pyt@#$hon cod#$%e in VS"
result = count_special_characters(str1)
print("Total special characters:", result)


# write a function to reverse the string 
str1 = "This is python code in VS"
def reverse_string(input_string):   
    return input_string[::-1]
result = reverse_string(str1)
print("Reversed string:", result)


