first_number = int(input("\nFirst number:"))
second_number = int(input("\nSecond number:"))

try:
    # print(5/0)
    answer = first_number / second_number
except ZeroDivisionError:
    # print("You can't divide by zero!")
    pass
else:
    print(answer)