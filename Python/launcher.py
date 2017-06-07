from keras.models import load_model

from evaluation import *
from game import Game
from negabeta_player import NegabetaPlayer
from newbie_player import NewbiePlayer
from q_player import QPlayer
from random_player import RandomPlayer

gamma = 0.9
epsilon = 0.1
epochs = 10000
date = "2017-06-07-18-03-09"

parameters = "-gamma-{}-epsilon-{}-epochs-{}-".format(gamma, epsilon, epochs)
directory = "C:\\Users\\Laouen\\PycharmProjects\\Awale\\QPlayers\\"

filename = directory + "qplayer" + parameters + date + ".model"

model = load_model(filename)

w = [0, 0, 0]

for i in range(1000):
    if i % 100 == 0:
        print(i)

    game = Game(QPlayer(model), RandomPlayer, debug=False)

    try:
        game.new_game()
        w[game.awale.winner] += 1
    except Exception as e:
        # game.display_board()
        # print(e)
        w[-1] += 1

print(w)

# game = Game(QPlayer(model), NegabetaPlayer(1, evaluation1), debug=False)
# game.new_game()
# game.display_result()
#
# game = Game(NewbiePlayer, QPlayer(model), debug=False)
# game.new_game()
# game.display_result()
