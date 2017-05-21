from game import Game
from awale_oop import Awale
from human_player import HumanPlayer
from random_player import RandomPlayer
from newbie_player import NewbiePlayer
from negamax_player import NegamaxPlayer
from negabeta_player import NegabetaPlayer
from q_player import QPlayer
from evaluation import *
from keras.models import load_model

model = load_model(
    "C:\\Users\\Laouen\\PycharmProjects\\Awale\\QPlayers\\qplayer_exploration_epochs20000_exploitation_epochs5000_gamma0.99_opponentNewbiePlayer.model")
w = [0, 0, 0]

# for k in range(1000):
#     if k % 100 == 0:
#         print(k)
#     game = Game(QPlayer(model), NewbiePlayer, debug=False)
#     try:
#         game.new_game()
#         w[game.awale.winner] += 1
#     except:
#         w[-1] += 1
#
# print(w)

game = Game(QPlayer(model), NewbiePlayer, debug=False)
game.new_game()
game.display_result()
