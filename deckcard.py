from enum import Enum
import random
from typing import Union, List


class Seed(Enum):
    SPADE = 0
    HEART = 1
    DIAMOND = 2
    CLUB = 3


class Card:

    def __init__(self, seed: Seed, value: int):
        self.seed = seed
        self.value = value
        self.max_value = 13

    def __str__(self):
        return covert_to_human_readable(self)

    def __ceil__(self) -> int:
        return self.max_value

    def __floor__(self) -> int:
        return 1

    def __eq__(self, other):
        return self.seed == other.seed and self.value == other.value

    def __hash__(self):
        return hash((self.seed, self.value))


class Deck:
    def __init__(self):
        self.deck = dict()
        self.max_value = 13
        self.reset()

    def reset(self):
        for seed in Seed:
            for value in range(1, self.max_value + 1):
                self.deck[Card(seed, value)] = True

    def draw_random(self, number_of_cards: int = 1) -> Union[Card, List]:

        cards = list()
        idx = 0

        while idx < number_of_cards:

            seed = random.choice(list(Seed))
            value = random.randint(1, self.max_value)

            if self.deck[Card(seed, value)]:
                card = Card(seed, value)
                cards.append(card)
                idx += 1
                self.deck[Card(seed, value)] = False

        if cards.__len__() == 1:
            return cards[0]
        return cards


def covert_to_human_readable(card: Card) -> str:

    if card.value == 11:
        card_value = "J"
    elif card.value == 12:
        card_value = "Q"
    elif card.value == 13:
        card_value = "K"
    else:
        card_value = str(card.value)

    if card.seed == Seed.SPADE:
        card_seed = "♠"
    elif card.seed == Seed.HEART:
        card_seed = "♥"
    elif card.seed == Seed.DIAMOND:
        card_seed = "♦"
    else:  # card.seed == Seed.CLUB:
        card_seed = "♣"

    return f"{card_seed}{card_value}"
