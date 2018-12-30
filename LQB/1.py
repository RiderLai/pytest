i = 1
sum = 0
while True:
    sum += 1 / i
    i += 1
    if sum >= 15:
        print(i)
        break
