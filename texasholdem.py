from gym import Env, spaces
from enum import Enum
from deckcard import Card, Seed, covert_to_human_readable, random_card
import random


class Player:
    def __init__(self, id: int, stack: float):
        self.id = id
        self.stack = stack
        self.cards = []
        self.is_active = False
        self.is_all_in = False
        self.is_dealer = False
        self.is_small_blind = False
        self.is_big_blind = False

    def __str__(self):
        return f"Player {self.id} has {self.stack} chips"

    def reset(self):
        self.cards = []
        self.is_active = False
        self.is_all_in = False
        self.is_dealer = False
        self.is_small_blind = False
        self.is_big_blind = False


class Action(Enum):
    FOLD = 0
    CALL = 1
    RAISE = 2


class Phase(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    SHOWDOWN = 4


class StateMachine(Enum):
    DRAW_CARD = 0
    DRAW_TWO_CARDS = 1
    DRAW_THREE_CARDS = 2
    ASK_ACTION = 3


def get_two_cards():
    return random_card(number_of_cards=2)


def get_one_cards():
    return random_card(number_of_cards=1)


class TexasHoldemEnv(Env):
    def __init__(self, number_of_players: int = 5, initial_stack: float = 1000, small_blind: float = 10):

        self.initial_stack = initial_stack
        self.players_id = [idx for idx in range(number_of_players)]
        self.players = [Player(player_id, initial_stack) for player_id in self.players_id]
        self.small_blind = small_blind
        self.big_blind = small_blind * 2.0

        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Discrete(3)

        self.players_active = None
        self.__table = {Phase.FLOP: None, Phase.TURN: None, Phase.RIVER: None}
        self.game_state = None
        self.stake = None

        # State of the game
        self.dealer_id = random.choice(self.players_id)

        self.reset()

    def _set_dealer(self, dealer_id: int):
        assert dealer_id > 0
        dealer_id = dealer_id % len(self.players)

        self.players[dealer_id].is_dealer = True

    def _set_small_blind(self, dealer_id: int) -> None:
        assert dealer_id > 0
        player_small_blind = (dealer_id + 1) % len(self.players)

        self.players[player_small_blind].is_small_blind = True

    def _set_big_blind(self, dealer_id: int) -> None:
        assert dealer_id > 0
        player_big_blind = (dealer_id + 2) % len(self.players)

        self.players[player_big_blind].is_big_blind = True

    def step(self, action):
        if self.game_state == Phase.PREFLOP:
            self.__table[Phase.FLOP] = [get_one_cards() for _ in range(3)]
            self.game_state = Phase.FLOP
        elif self.game_state == Phase.FLOP:
            self.__table[Phase.TURN] = get_one_cards()
            self.game_state = Phase.TURN
        elif self.game_state == Phase.TURN:
            self.__table[Phase.RIVER] = get_one_cards()
            self.game_state = Phase.END
        # self.game_state == Phase.END:
        # DO NOTHING

        return self.__table, 0, False, {}

    # TODO: fix the output of this function
    def reset(self):
        self.__table = {Phase.FLOP: None, Phase.TURN: None, Phase.RIVER: None}
        self.game_state = Phase.PREFLOP

        self.players_active = [idx for idx, player in enumerate(self.players) if player.is_active]

        # Player reset
        for player_id, player in enumerate(self.players):
            self.players[player_id].reset()

        # New dealer
        self.dealer_id = (self.dealer_id + 1) % len(self.players)

        self._deal_new_cards()

        # Set the stake
        self.stake = 0

        if self.players[self.dealer_id + 1].stack < self.small_blind:
            self.stake += self.players[self.dealer_id + 1].stack

            self.players[self.dealer_id + 1].is_all_in = True
            self.players[self.dealer_id + 1].stack = 0
        else:
            self.stake += self.small_blind

        if self.players[self.dealer_id + 2].stack < self.big_blind:
            self.stake += self.players[self.dealer_id + 2].stack

            self.players[self.dealer_id + 2].is_all_in = True
            self.players[self.dealer_id + 2].stack = 0
        else:
            self.stake += self.big_blind

        # Set the active players
        for player in self.players:
            player.is_active = True

        return self.__table

    def _deal_new_cards(self):
        self._set_small_blind(self.dealer_id)
        self._set_big_blind(self.dealer_id)

        for player in self.players:
            player.cards = get_two_cards()

    def __str__(self) -> str:
        if self.__table[Phase.FLOP]:
            print(f"{self.__table[Phase.FLOP][0]} "
                  f"{self.__table[Phase.FLOP][1]} "
                  f"{self.__table[Phase.FLOP][2]}", end='')
        else:
            print("_ _ _", end='')

        if self.__table[Phase.TURN]:
            print(f" {covert_to_human_readable(self.__table[Phase.TURN])}", end='')
        else:
            print(" _", end='')

        if self.__table[Phase.RIVER]:
            print(f" {covert_to_human_readable(self.__table[Phase.RIVER])}")
        else:
            print(" _")

        return ""

        # TODO: used for testing

    def random_state(self):
        self.__table[Phase.FLOP] = [random_card(),
                                    random_card(),
                                    random_card()]
        self.__table[Phase.TURN] = random_card()
        self.__table[Phase.RIVER] = random_card()

    def render(self, mode='human', close=False):
        pass