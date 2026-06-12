def show (n):
    print(n)
    if (n == 0):
        return

    show (n - 1)

show(6)