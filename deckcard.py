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


def random_card(number_of_cards: int = 1) -> Union[Card, list]:

    cards = list()

    for idx in range(number_of_cards):
        card = Card(random.choice(list(Seed)), 1)
        card.value = random.randint(1, card.max_value)
        cards.append(card)

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
