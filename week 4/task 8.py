i=1
while i <= 5:
    j=0
    while(j<=6-i):
        print(" ", end=" ")
        j=j+1
    while (j<(i*2)-1):
        print("*", end=" ")
        j=j+1
    print()
    i=i+1