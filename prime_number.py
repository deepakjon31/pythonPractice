"""
1. Find a prime number
"""

a = input("Enter a first number:")
b = input("Enter a second number:")

for i in range(int(a), int(b)+1):
    k = 0
    for j in range(2, i//2 + 1):
        if i % j == 0:
            k += 1
    if k == 0:
       print(i)
