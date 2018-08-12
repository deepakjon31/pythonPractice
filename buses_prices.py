"""
Question
---------------
Which Bus To Take? :O
Lolita lives very far away from her office. She needs to take a bus daily in order to reach her destination; however direct bus services are not available from her home to the destination. So she needs to take several buses in order to reach her destination.

The cost of changing buses is calculated in a weird way which will be explained below. Suppose she takes n buses b0, b1, …, bn-1.

Suppose the cost of traveling in bus bi is given by ci.

And suppose she takes the buses in the same order i.e. first travels by bus b0 then b1 and so on.

The cost of the whole trip is given by the following calculation:

Let Sk = Sk-1 + ck

where n - 1 >= k > 1.

And let S1 = c0 + c1

Then the total cost of the trip is given by the sum S1 + S2 + … + Sn-1.

Example

Suppose she takes 5 buses to work, bus A, B, C, D and E. And suppose she takes the buses in order i.e. travels by bus A,
gets off and then travels by bus B and so on.

Suppose also the cost of travelling each bus is given by 10, 3, 7, 1, 8. (All in Rs.)

Then:

S1 = c0 + c1 = 10 + 3 = 13

S2 = S1 + c2 = 13 + 7 = 20

S3 = S2 + c3 = 20 + 1 = 21

S4 = S3 + c4 = 21 + 8 = 29

The total cost of the trip is given by S1 + S2 + … + S4 = 13 + 20 + 21 + 29 = 83

So given the number of buses she has to take to reach her destination, and the cost of travel for each bus, find out
the minimum possible total cost of travel.

NOTE: She can choose the buses in any order; but she needs to ride all buses. Also, if she takes only one bus, the cost of the trip is the cost
of traveling on that bus.

Input Format

The first line of input contains an integer T which is the number of test cases.

For each test case, there will be two lines of input.

The first line of input will contain an integer N. This is the number of buses she takes.

The next line will contain N space separated integers representing the cost of travel for each bus.

Output Format

For each test case, output the minimum possible cost of travel. The answer for each test case should be
on a different line.

Constraints

0 <= T <= 1000 (This is the number of test cases)

0 < N <= 2000 (This is the number of buses available)

0 < M <= 2000 (This is the cost of travel for each of the N buses)

Sample Input

2
4
6 5 9 4
3
8 6 2
Sample Output

48
24
Explanation

In the first test case, Lolita first takes the bus which costs 4 and then takes the bus which costs 5 rupees. The third bus she takes is the one
that costs Rs. 6. The last bus she takes will be the one that costs 9 rupees. The total cost, if you calculate it as above, will be Rs. 48.
You can go through the second test case and assure yourself that the minimum cost is Rs. 24.

SAMPLE STDIN 1

2
4
6 5 9 4
3
8 6 2
SAMPLE STDOUT 1

48
24
"""

for test in range(int(input('number of test cases: '))):
    price_list = []
    bus_no = int(input("number of Buses: "))
    buses = sorted(list(map(int, input('enter bus prices with space: ').split())))
    if bus_no == len(buses):
        sum = buses[0]
        for i in range(1, len(buses)):
            sum = sum + buses[i]
            price_list.append(sum)
    summ = 0
    for i in price_list:
        summ = summ + i
    print(summ)


