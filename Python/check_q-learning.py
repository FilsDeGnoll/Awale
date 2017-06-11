import numpy
import time
from keras.models import load_model

from evaluation import *
from game import Game
from negabeta_player import NegabetaPlayer
from newbie_player import NewbiePlayer
from q_player import QPlayer, get_state
from random_player import RandomPlayer

gamma = 0.9
epsilon = 0.1
epochs = 35000
date = "2017-06-10-18-35-43"

parameters = "-gamma-{}-epsilon-{}-epochs-{}-".format(gamma, epsilon, epochs)
directory = "C:\\Users\\Laouen\\PycharmProjects\\Awale\\QPlayers\\"

filename = directory + "qplayer" + parameters + date + ".model"

model = load_model(filename)

# Test sur un plateau

# board = numpy.array([1, 0, 3, 7, 0, 3, 2, 3, 1, 3, 2, 2])
# state = get_state(board)
#
# print(model.predict(numpy.array([state])))

# Calcul du temps d'exécution moyen

# t = time.clock()
#
# for i in range(10000):
#     board = numpy.random.randint(0, 12, 12)
#     state = get_state(board)
#
#     model.predict(numpy.array([state]))
#
# t = time.clock() - t
# print(t/10000)

# Test du modèle

victoires = 0
defaites = 0
egalites = 0
depassements = 0
erreurs = 0

for i in range(1000):
    if i % 100 == 0:
        print(i)

    game = Game(QPlayer(model), RandomPlayer, debug=False)

    try:
        game.new_game()
        if game.awale.winner == 0:
            victoires += 1
        elif game.awale.winner == 1:
            defaites += 1
        else:
            egalites += 1
        if game.moves_count == game.max_count:
            depassements += 1
    except:
        erreurs += 1

print("Victoires = {}, défaites = {}, égalités = {}, dépassements = {}, erreurs = {}".format(victoires, defaites,
                                                                                             egalites, depassements,
                                                                                             erreurs))

# game = Game(QPlayer(model), NegabetaPlayer(1, evaluation1), debug=False)
# game.new_game()
# game.display_result()
#
# game = Game(NewbiePlayer, QPlayer(model), debug=False)
# game.new_game()
# game.display_result()
