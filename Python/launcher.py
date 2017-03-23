from game import Game
from awale import Awale
from human_player import HumanPlayer
from random_player import RandomPlayer
from newbie_player import NewbiePlayer
from negamax_player import NegamaxPlayer
from negabeta_player import NegabetaPlayer
from evaluation import *
import time

game = Game(NegabetaPlayer(6,evaluation2), NegabetaPlayer(7, evaluation3), debug=False)
t = time.clock()
game.new_game()
t = time.clock() - t
print("Durée de la partie en minutes :", (t / 60))
game.display_result()
