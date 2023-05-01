"""Main Example."""
from texasholdem import TexasHoldemEnv

if __name__ == '__main__':
    env = TexasHoldemEnv()
    print(env)
    env.step(1)
    print(env)
    env.step(1)
    print(env)
    env.step(1)
    print(env)

    env.reset()
    env.step(1)
    print(env)
    env.step(1)
    print(env)
    env.step(1)
    print(env)
