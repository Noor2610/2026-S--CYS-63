large_number = lambda a, b: a if a > b else b

def print_table(num, limit):
    for i in range(1, limit + 1):
        print(f"{num} x {i} = {num * i}")
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))
limit = int(input("Enter table range: "))
big = large_number(num1, num2)

print("Larger number is:", big)
print("Table of larger number: ")

print_table(big, limit)