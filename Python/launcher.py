from evaluation import evaluation1, evaluation2
from game import Game
from human_player import HumanPlayer
from newbie_player import NewbiePlayer
from negabeta_player import NegabetaPlayer

game = Game(HumanPlayer, NegabetaPlayer(10, evaluation1), debug=True)
game.new_game()
