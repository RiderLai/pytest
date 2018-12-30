import random


class BingoCage:
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(x=self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        return self.pick()


bingo = BingoCage(range(10))
print(type(bingo))

print(callable(bingo))

for i in range(11):
    print(bingo())

# print(bingo())
# print(bingo())
# print(bingo())
# print(bingo())
# print(bingo())
# print(bingo())
# print(bingo())
# print(bingo())
# print(bingo())
# print(bingo())
# print(bingo())