# import random
# emp_name = ["John", "Jane", "Doe", "Smith", "Emily"]
# res=random.choice(emp_name)
# print("Randomly selected employee name:", res)



import random
# emp_name = ["John", "Jane", "Doe", "Smith", "Emily"]
# weight = [2,3,1,0,4]  # Assign weights to each employee name
# res=random.choices(emp_name, weights=weight, k=4)
# print("Randomly selected employee name:", res)



# res=random.random()*100000000
# print("Random number between 0 and 1:", res)
# print(int(res))


# res=random.randint(0, 10)
# rand_range = random.randrange(0, 10)
# print("Random number between 0 and 10:", res)
# print("Random number from range 0 to 10:", rand_range)



# user max attempt = 6
# each attempt random number generate
# random number generate sum
# fix_vaule = 150


# ''' wap to a user play a game where user has maximum 6 attempts to guess a random number if the sum of 
# all random number generated in each attempt is equal to the fixed value then user wins otherwise user loses
# and print the sum of all random number generated in each attempt when user reach 150 then close game show you win otherwise you lose '''


# Sample()
# emp_name = ["John", "Jane", "Doe", "Smith", "Emily"]
# res=random.sample(emp_name, k=3)
# print(res)


# shuffle()
# emp_name = ["John", "Jane", "Doe", "Smith", "Emily"]
# random.shuffle(emp_name)
# print(emp_name)



# generate coupon code in which first 4 character is alphabets and last 4 character is numbers 10 times generate coupon code and print it

# def generate_coupon_code():
#     alpha_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
#     number_code = ''.join(random.choices('0123456789', k=4))
#     coupon_code = alpha_code + number_code
#     return coupon_code

# for _ in range(10):
#     print(generate_coupon_code())
    
    
    

# alpha_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
# number_code = ''.join(random.choices('0123456789', k=4))
# coupon_code = alpha_code + number_code
# print(coupon_code)


# def generate_coupon_code():
#     a_to_z = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#     num = '0123456789'
#     char = "".join(random.choices(a_to_z, k=4))
#     num = random.random()*10000
#     res = char.upper() + str(int(num))
#     print(res)
   
# for i in range(10):
#     generate_coupon_code()



# def generate_coupon_code():
#     import string
#     print("".join(random.choices(string.ascii_uppercase, k=4)) + "".join(random.choices(string.digits, k=4)))
   
# for i in range(10):
#     generate_coupon_code()
    
    
