from itertools import combinations_with_replacement as cr
import string

alpa = list(zip(string.ascii_lowercase,list(range(1,27))))

s = ''
for t in range(int(input())):
    n, k = map(int, input().split())
    pr = [i for i in list(cr(range(1, 27), n)) if sum(i) == k][0]
    for i in pr:
        for a in alpa:
            if i == a[1]:
                s = s + a[0]
    print(s)
    s = ''
