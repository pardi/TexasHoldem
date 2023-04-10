from gym import Env, spaces
from enum import Enum
from deckcard import Card, Seed, covert_to_human_readable, random_card
import random


class Player:
    def __init__(self, name: str, stack: int, position: int):
        self.name = name
        self.stack = stack
        self.position = position
        self.cards = []
        self.is_folded = False
        self.is_all_in = False
        self.is_dealer = False
        self.is_small_blind = False
        self.is_big_blind = False
        self.is_button = False
        self.is_active = False
        self.is_winner = False
        self.is_loser = False
        self.is_tie = False


class Action(Enum):
    FOLD = 0
    CALL = 1
    RAISE = 2


class Phase(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3


def get_two_cards():
    return random_card(number_of_cards=2)


def get_one_cards():
    return random_card(number_of_cards=1)


class TexasHoldemEnv(Env):
    def __init__(self, number_of_players: int = 5):
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Discrete(3)
        self.__state = {Phase.FLOP: None, Phase.TURN: None, Phase.RIVER: None}
        self.dealer_id = 0
        self.players_id = [idx for idx in range(number_of_players)]

    def step(self, action):
        if action == 0:
            self.__state = 0
        elif action == 1:
            self.__state = 1
        elif action == 2:
            self.__state = 2
        else:
            raise ValueError("Invalid action")
        return self.__state, 0, False, {}

    # TODO: fix the output of this function
    def reset(self):
        self.__state = 0
        return self.__state

    def __str__(self) -> str:
        if self.__state[Phase.FLOP]:
            print(f"{self.__state[Phase.FLOP][0]} "
                  f"{self.__state[Phase.FLOP][1]} "
                  f"{self.__state[Phase.FLOP][2]}", end='')
        else:
            print("_ _ _", end='')

        if self.__state[Phase.TURN]:
            print(f" {covert_to_human_readable(self.__state[Phase.TURN])}", end='')
        else:
            print(" _", end='')

        if self.__state[Phase.RIVER]:
            print(f" {covert_to_human_readable(self.__state[Phase.RIVER])}")
        else:
            print(" _")

        return ""

        # TODO: used for testing

    def random_state(self):
        self.__state[Phase.FLOP] = [random_card(),
                                    random_card(),
                                    random_card()]
        self.__state[Phase.TURN] = random_card()
        self.__state[Phase.RIVER] = random_card()

    def render(self, mode='human', close=False):
        pass