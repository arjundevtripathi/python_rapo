# a=10
# b=2
# c=a/b
# print(c)


try:
    a=10
    b=0
    c=a/b
except Exception as e:
    print("Exception",e)
