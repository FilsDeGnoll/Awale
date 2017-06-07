from evaluation import evaluation1, evaluation2
from game import Game
from newbie_player import NewbiePlayer
from negabeta_player import NegabetaPlayer

game = Game(NewbiePlayer, NegabetaPlayer(2, evaluation2), debug=True)
game.new_game()

game = Game(NegabetaPlayer(1, evaluation1), NegabetaPlayer(2, evaluation2))
game.new_game()