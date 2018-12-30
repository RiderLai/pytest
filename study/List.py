a = 1

'''test1'''

bicycles = ['trek', 'cannondale', 'redline', 'specialized', 'test']
print(bicycles)
print(bicycles[0])
print(bicycles[1].title())
print(bicycles[-1])
print("My first bicycle was a " + bicycles[0].title() + ".")
print("----------------------------------------------")

'''test2'''

# motorycles = ['honda', 'yamaha', 'suzuki']
# print(motorycles)
# # motorycles[0] = 'ducati'
# motorycles.append('ducati')
# print(motorycles)

motorycles = []
motorycles.append('honda')
motorycles.append('yamaha')
motorycles.append('suzuki')
motorycles.insert(0, 'ducati')
print(motorycles)

# del motorycles[1]
# print(motorycles)

# motorycles.pop(2)
# print(motorycles)

# motorycles.remove('honda')
# print(motorycles)

# motorycles.sort()
# print(motorycles)
#
# motorycles.sort(reverse=True)
# print(motorycles)

# print(sorted(motorycles,reverse=True))
# print(motorycles)

# motorycles.reverse()
# print(motorycles)

# print(len(motorycles))

print("----------------------------------------------")

'''test3'''
# magicians = ['alice', 'david', 'carolina']
# for magician in magicians:
#     print(magician)
#
# for item in range(1, 5):
#     print(item)

# i = list(range(1, 5))
# print(i)
#
# squares = [value**2 for value in range(1, 5)]
# print(squares)

even_numbers = list(range(2, 11, 2))
print(even_numbers)

even_numbers.append(0)
# even_numbers.append('a')
print(even_numbers)
print(max(even_numbers))
print(min(even_numbers))
print(sum(even_numbers))

print(even_numbers[1:3])
print(even_numbers[:8])
print(even_numbers[1:])
print(even_numbers[-3:])
print(even_numbers[-8:])

print("----------------------------------------------")

'''test4'''
my_foods = ['pizza', 'falafel', 'carrnt cake']
friden_food = my_foods[:2]

my_foods.append('cannoli')
friden_food.append('ice cream')

print(my_foods)
print(friden_food)

print("----------------------------------------------")

'''test5'''

dimensions = (200, 50)
print(dimensions[0])
print(dimensions[1])

for demension in dimensions:
    print(demension)