file_path = r'c:\n'

'''test1'''
with open('pi.txt') as file_object:
    # contents = file_object.read()
    # print(contents)
    lines = file_object.readlines()
    # for line in file_object:
    #     print(line)

for line in lines:
    print(line)

print("--------------------------")

'''test2'''
with open('pi.txt') as file_object1:
    contents = file_object1.read()

print(contents[:52])

print('141' in contents)

print("--------------------------")

'''test3'''
# w写入 a追加
with open('pi.txt', 'a') as file_object2:
    file_object2.write("\nI love programming.")
    file_object2.writelines(['\n one', '\n two'])