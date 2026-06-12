import random
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowercase = "abcdefghijklmnopqrstuvwxyz"
digits = "0123456789"
special = "!@#$%^&*()_+-=[]{}|;:,.<>?/"
length = input("Enter password length: ")
use_upper = input("Include uppercase letters? (y/n): ")
use_lower = input("Include lowercase letters? (y/n): ")
use_digits = input("Include digits? (y/n): ")
use_special = input("Include special characters? (y/n): ")
characters = ""
if use_upper.lower() == "y":
    characters += uppercase
if use_lower.lower() == "y":
    characters += lowercase
if use_digits.lower() == "y":
    characters += digits
if use_special.lower() == "y":
    characters += special
if characters == "":
    print("Error: You must select at least one character type!")
else:
    password = " "
    for i in range(length):
        password += random.choice(characters)
    print("Generated Password:", password)