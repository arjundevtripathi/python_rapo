# 8. Find the repetitive elements in the list [1,2,3,4,56,1,22,23,33,23, 56].
li = [1, 2, 3, 4, 56, 1, 22, 23, 33, 23, 56]

seen = []
duplicates = []

for num in li:
    if num in seen:
        if num not in duplicates:
            duplicates.append(num)
    else:
        seen.append(num)

print(duplicates)