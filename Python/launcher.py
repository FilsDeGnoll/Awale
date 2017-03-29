from game import Game
from awale import Awale
from human_player import HumanPlayer
from random_player import RandomPlayer
from newbie_player import NewbiePlayer
from negamax_player import NegamaxPlayer
from negabeta_player import NegabetaPlayer
from q_player import QPlayer
from evaluation import *
from keras.models import load_model

# TODO: à modifier.
p = [0, 0, 0]
model = load_model()
for k in range(1000):
    if k % 100 == 0:
        print(k)
    game = Game(QPlayer(model), RandomPlayer(), debug=False)
    try:
        game.new_game()
        p[game.awale.winner] += 1
    except:
        game.display_board()
        p[-1] += 1

print(p)
