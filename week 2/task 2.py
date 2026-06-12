s = input("Enter a sentence: ")

v = 0
c = 0

for ch in s:
    ch = ch.lower()
    if ch.isalpha():
        if ch in "aeiou":
            v += 1
        else:
            c += 1
print("Number of Vowels =", v)
print("Number of Consonants =", c)