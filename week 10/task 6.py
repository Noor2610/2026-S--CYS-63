t=int(input("enter total marks:"))
o=int(input("enter obtained marks:"))
p=o/t*100
print("total percentage is: ",p)
if(p>=90):
    print("A+")
elif(p>=85):
    print("A-")
elif(p>=80):
    print("B+")
elif(p>=75):
    print("B-")
elif(p>=70):
    print("C+")
elif(p>=65):
    print("C-")
elif(p>=60):
    print("D+")
elif(p>=55):
    print("D-")
else:
    print("F")
if(p>=70):
    print("yeah! go for it")
else:
    print("keep going, u are almost there")