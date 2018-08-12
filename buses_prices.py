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


