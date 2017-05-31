import numpy
from game import Game
from awale_oop import Awale
from human_player import HumanPlayer
from random_player import RandomPlayer
from newbie_player import NewbiePlayer
from negamax_player import NegamaxPlayer
from negabeta_player import NegabetaPlayer
from q_player import QPlayer, get_state
from evaluation import *
from keras.models import load_model

model1 = load_model("C:\\Users\\Laouen\\PycharmProjects\\Awale\\QPlayers\\qplayer_epochs5000_gamma0.9_epsilon0.1.model")
model2 = load_model("C:\\Users\\Laouen\\PycharmProjects\\Awale\\QPlayers\\qplayer_epochs4999_gamma0.9_epsilon0.1.model")

# w = [0, 0, 0]
#
# for i in range(1000):
#     if i % 100 == 0:
#         print(i)
#     game = Game(QPlayer(model), RandomPlayer, debug=False)
#     try:
#         game.new_game()
#         w[game.awale.winner] += 1
#     except:
#         w[-1] += 1
#
# print(w)
#
# game = Game(QPlayer(model1), NewbiePlayer, debug=True)
# game.new_game()
# game.display_result()

# game = Game(NewbiePlayer, QPlayer(model), debug=True)
# game.new_game()
# game.display_result()

board = numpy.array([1, 0, 3, 7, 0, 3, 2, 3, 1, 3, 2, 2])
state = get_state(board)
print(model1.predict(numpy.array([state])))
