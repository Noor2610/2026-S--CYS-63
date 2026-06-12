start = int(input("Enter starting number: "))
end = int(input("Enter ending number: "))
prime_sum = 0
print("Prime numbers in the given range are:")
for num in range(start, end + 1):
    if num > 1:
        is_prime = True
        for i in range(2, num):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            print(num, end=" ")
            prime_sum += num

print("\nSum of prime numbers =", prime_sum)