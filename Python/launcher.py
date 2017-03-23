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
import numpy
from keras.models import load_model

def get_state(board, player):
    board = numpy.copy(board)
    if player == 1:
        board = numpy.array([board[(i + 6) % 12] for i in range(12)])

    state = -numpy.ones(32 * 12)
    for i in range(12):
        for j in range(board[i]):
            state[i * 32 + j] = 1
    return state

def get_input_array(board, score, player):
    state = get_state(board, player)
    return state


def get_move(input_array, model):
    [q_values] = model.predict(numpy.array([input_array]))
    return numpy.argmax(q_values)

model = load_model("qlearner1903.model")
winners = []
n = 1000
for _ in range(n):
    # t = time.clock()
    awale = Awale()
    moves_count = 0
    max_count = 400
    player = 0

    while awale.winner == -2 and moves_count < max_count:
        moves_count += 1
        if player == 0:
            board = awale.board
            score = awale.score
            input_array = get_input_array(board, score, player)
            move = get_move(input_array, model)
        else:
            move = RandomPlayer.get_move(awale, 1)
        if awale.can_play(player, move):
            awale.play(player, move)
            awale.check_winner(player)
        else:
            winners.append(-3)
            break
        player = 1 - player
    # t = time.clock() - t
    if awale.score[0] >= 24 or awale.score[1] >= 24:
        winners.append(awale.winner)
winners = numpy.array(winners)
print("coups invalides = {}".format((winners == -3).sum() * 100 / n))
print("victoires = {}".format((winners == 0).sum() * 100 / n))
print("défaites = {}".format((winners == 1).sum() * 100 / n))
# print("Durée de la partie en minutes :", (t / 60))
