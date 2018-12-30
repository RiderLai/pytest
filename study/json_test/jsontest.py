import json


class Test:
    """test"""

    def __init__(self, _numbers, _name):
        self.numbers = _numbers
        self.name = _name


numbers = [3, 5, 7, 9]
name = 'Rider'

# Test类需要 可json序列化
test_object = Test(numbers, name)

filename = 'jsonfile.txt'

'''write'''
with open(filename, 'w') as file_object:
    json.dump(numbers, file_object)

'''read'''
# with open(filename) as file_object:
#     numbers = json.load(file_object)
#
# print(numbers)
# print(type(numbers))