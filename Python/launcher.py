from game import Game
from awale import Awale
from human_player import HumanPlayer
from random_player import RandomPlayer
from newbie_player import NewbiePlayer
from negamax_player import NegamaxPlayer
from negabeta_player import NegabetaPlayer
from q_player import QPlayer
from evaluation import *
import time
from keras.models import load_model

model = load_model("qlearner1903.model")
game = Game(QPlayer(model), RandomPlayer, debug=True)
t = time.clock()
game.new_game()
t = time.clock() - t
print("Durée de la partie en minutes :", (t / 60))
