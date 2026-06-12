num = input("Enter a number: ")

if num == num[::-1]:
    print(num, "is a Palindrome Number")
else:
    print(num, "is Not a Palindrome Number")