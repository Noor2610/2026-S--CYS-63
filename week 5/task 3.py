to_upper = lambda s: s.upper()
def invert(text):
    return text[::-1]
text = input("Enter a string: ")
upper_text = to_upper(text)
print("Uppercase String:", upper_text)
reversed_text = invert(upper_text)
print("Reversed String:", reversed_text)