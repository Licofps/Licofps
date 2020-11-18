n = int(input())
m = n

for x in range(n):
    for y in range(0, n + 1):
        print(y, end="")
    print()
    n -= 1

print(0)

for c in range(m, -1, -1):
    print(c, end = "")
print()
