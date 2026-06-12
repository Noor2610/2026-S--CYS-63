y=int(input("enter number of students"))
i=1
while (i<=y):
    n=input("enter your name")
    a=int(input("enter obtained marks"))
    b=int(input("enter total marks"))
    c=a/b*100
    print(c)
    if c>=90:
        print("A")
    elif c>=85:
        print("A-")
    elif c>=80:
        print("B+")
    elif c>=75:
        print("B-")
    elif c>=70:
        print("C+")
    elif c>=65:
        print("C-")
    elif c>=60:
        print("D+")
    elif c>=55:
        print("D-")
    else :
        print("F")
    i=i+1