def keyy(a):
    return a[1]


def run(k=2, i=1):
    if i==8:
        print(k)
        return

    list = [(j, abs((k+j*10**(-i))**(k+j*10**(-i)) - 20)) for j in range(10)]
    list_min = min(list, key=keyy)
    a = (list_min[0]-1)*10**(-i)
    run(k=k+(list_min[0]-1)*10**(-i), i=i+1)

run()