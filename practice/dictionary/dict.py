# wap to create a dictionary with key values name and marks and print the dictionary
# student = {"name": "Alice", "marks": 85} 
# print(student)
# student["marks"] = 90
# print(student)


stu_marks =  {'arjun': 90, 'vijay': 80, 'sachin': 70 }
new_marks = {'sneha': 95, 'rahul': 85}
print(stu_marks)
stu_marks.update(new_marks)
print(stu_marks)


profile = {
    'aman':{
        'address':['123 Main St', '456 Oak St', '789 Pine St'],
        'phone': ['123-456-7890', '987-654-3210'],
        'hobbies': ['reading', 'traveling', 'cooking'],
        'password': {'instagram': 'aman123', 'facebook': 'aman456', 'twitter': 'aman789'}
    },
    
    'sneha':{
        'address':['321 Elm St', '654 Maple St', '987 Cedar St'],
        'phone': ['555-123-4567', '555-987-6543'],
        'hobbies': ['painting', 'dancing', 'gardening'],
        'password': {'instagram': 'sneha123', 'facebook': 'sneha456', 'twitter': 'sneha789'}
    }   
}

result = profile['aman']['address'][1]
result = profile['sneha']['password']['facebook']

print(result)