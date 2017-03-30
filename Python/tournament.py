# TODO: Comparer evaluation 3 et les autres URGENT
# TODO: Comparer temps d'éxécution Negabeta/Negamax OSEF
# TODO: Nombre de coup URGENT
from evaluation import *
from game import Game
from negabeta_player import NegabetaPlayer

rep = [[] for _ in range (10)]
for i in range(1, 11):
    for j in range(1, 11):
        game = Game(NegabetaPlayer(i, evaluation3), NegabetaPlayer(j, evaluation1), debug=False)
        game.new_game()
        rep[i-1].append(game.moves_count)
    print(i)
print (rep)