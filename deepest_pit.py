"""
From a test of a (in)famous coding-site: given a zero-indexed array of integers A[N], we can define a "pit" (of this array) a triplet of integers (P,Q,R) such that they follow these rules:

0 ≤ P < Q < R < N

A[P] > A[P+1] > ... > A[Q] (strictly decreasing) and

A[Q] < A[Q+1] < ... < A[R] (strictly increasing).

We can also define the depth of this pit as the number

min{A[P] − A[Q], A[R] − A[Q]}.

You should write a Java method (function) deepest_pit(int[] A) which returns the depth of the deepest pit in array A or -1 if it does not exit.
"""
def recursiveInc(c, A):
    if A[c] < A[c+1]:
        return c
    else:
        return recursiveInc(c+1, A)

def recursiveDec(c, A):
    l = len(A)
    if c < l-1:
        if A[c] > A[c+1]:
            return  c
        else:
            return recursiveDec(c+1, A)
    else:
        return c

def deepest_pip(A):
    n = len(A)
    pitlist = []
    for p in range(0, n - 1):
        q = recursiveInc(p, A)
        if p < q:
            r = recursiveDec(q, A)
            print("p:{} q:{} r:{}".format(str(p),str(q),str(r)))
            if q < r:
                print("(" + str(A[p]) + "," + str(A[q]) + "," + str(A[r]) + ")")
                aa = A[p] - A[q]
                bb = A[r] - A[q]
                pitlist.append(min(aa, bb))
    if len(pitlist) > 0:
        pitlist.sort()
        return pitlist.pop()
    else:
        return  -1

def main():
    eList = [0, 1, 3, -2, 0, 1, 0, -3, 2, 3]
    print("max pit value: ", str(deepest_pip(eList)))


main()
