a = 0

'''test1'''
# message = input("Tell me something, and I will repeat it back to you:")
# print(message)

'''test2'''
current_number = 1
while current_number <= 5:
    print(current_number)
    current_number += 1

print("----------------------------------------------")

# prompt = "\nTell me something, and I will repeat it back to you:"
# prompt += "\nEnter 'quit' to end the program."
# message = ""
# while message != 'quit':
#     message = input(prompt)
#     print(message)

# while True:
#     print(1)

'''test3'''
pets = ['dog', 'cat', 'goldfish', 'cat', 'dog', 'rabbit']
print(pets)
pets.remove('cat')
print(pets)
print('cat' in pets)
print("----------------------------------------------")

'''test4'''
responses = {}

polling_active = True

while polling_active:
    name = input("\nWhat is your name?")
    response = input("Which mountain would you like to climb someday?")

    responses[name] = response

    repeat = input("Would you like to let another person respond?(yes/no)")
    if repeat == 'no':
        polling_active = False

print("\n--- Poll Results ---")
for name,response in responses.items():

    print(name + " would like to climb " + response + ".")