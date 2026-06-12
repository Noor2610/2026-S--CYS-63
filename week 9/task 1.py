try:
    age = int(input("Enter your age: "))
    print(f"Your age is {age}")
except ValueError:
    print("Please enter a number, not letters!")