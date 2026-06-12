import math
import cmath  # Used for imaginary roots
a = float(input("Enter value of a: "))
b = float(input("Enter value of b: "))
c = float(input("Enter value of c: "))
D = b**2 - 4*a*c
print("Discriminant =", D)
if D == 0:
    print("Roots are real, equal and rational.")
    root1 = (-b + math.sqrt(D)) / (2*a)
    root2 = (-b - math.sqrt(D)) / (2*a)
elif D > 0:
    print("Roots are real, distinct and irrational.")
    root1 = (-b + math.sqrt(D)) / (2*a)
    root2 = (-b - math.sqrt(D)) / (2*a)
else:
    print("Roots are imaginary.")    
    root1 = (-b + cmath.sqrt(D)) / (2*a)
    root2 = (-b - cmath.sqrt(D)) / (2*a)
print("Root 1 =", root1)
print("Root 2 =", root2)