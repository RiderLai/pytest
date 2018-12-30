import collections
from random import choice

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, item):
        return self._cards[item]


# frenchdeck = FrenchDeck()
# print(len(frenchdeck))
# print(frenchdeck[1])
# print(frenchdeck[0])
# print(frenchdeck[-1])
#
# for card in frenchdeck:
#     print(card)

suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]


for card in sorted(FrenchDeck(), key=spades_high):
    print(card)

print('----------------------------------------------')

for card in FrenchDeck():
    print(card)

print('----------------------------------------------')

print(choice(FrenchDeck()))

# a = FrenchDeck()[0] = Card(rank='1',suit='a')
# print(a)
# print(type(a))