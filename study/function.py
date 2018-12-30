# from pizza import make_pizza as makep
import study.pizza as pizza


def parting_line():
    print("-------------------------------------")


def greet_user(username):
    """显示问候语"""
    # print("Hello World!")
    print("Hello, " + username.title() + "!")


def describe_pet(pet_name, animal_type='dog'):
    """显示宠物信息"""
    print("\nI have a " + animal_type + ".")
    print("My " + animal_type + "'s name is " + pet_name.title() + ".")


def get_formatted_name(first_name, last_name):
    """返回一个整洁的姓名"""
    full_name = first_name + " " + last_name
    return [full_name]


def greet_users(names):
    """向列表中的每位用户都发出简单的问候"""
    # for name in names:
    #     print(name)
    names.pop()


def test(**a):
    print(a)


greet_user("Rider")
parting_line()

describe_pet('harry', 'hamster')
describe_pet(animal_type='dog', pet_name='a')
describe_pet(pet_name='aa')
parting_line()

musician = get_formatted_name('lai', 'yinfeng')
print(musician)
parting_line()

usernames = ['hannah', 'ty', 'margot']
print(usernames)
greet_users(usernames[:]) # greet_users(usernames)
print(usernames)
parting_line()

# test("aaa", "213")
test(aaa="a", bbb="b")
parting_line()

pizza.make_pizza(16, 'mushrooms', 'green peppers', 'extra cheese')