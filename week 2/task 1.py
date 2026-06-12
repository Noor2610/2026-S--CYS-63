b = input("Enter a binary number: ")
d = 0
p=0
for i in reversed(b):
    d += int(i) * (2 ** p)
    p += 1
print("Decimal Equivalent =", d)