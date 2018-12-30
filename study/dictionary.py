a = 1

'''test1'''
alien_0 = {'color': 'green', 'points': 5}
print(alien_0['color'])
print(alien_0['points'])

alien_0['a'] = 'a'
print(alien_0['a'])

print(alien_0)

# alien_0['color'] = 'red'
# print(alien_0)

# del alien_0['color']
# print(alien_0)
alien_0[1] = 1

for key, value in alien_0.items():
    print("key:" + str(key))
    print("value:" + str(value) + "\n")

print("----------------------------------------------")

'''test2'''
favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python'
}

friends = ['phil', 'sarah']

for name in favorite_languages.keys():
    print(name.title())

    if name in friends:
        print("Hi " + name.title() +
              ", I see your favorite language is " +
              favorite_languages[name].title() + "!")

print()

for name in sorted(favorite_languages.keys()):
    print(name.title() + ", thank you for taking the poll.")

print("----------------------------------------------")

'''test3'''
alien_1 = {'color': 'red', 'points': 15}
alien_2 = {'color': 'yellow', 'points': 10}

aliens = [alien_0, alien_1, alien_2]

for alien in aliens:
    print(alien)
