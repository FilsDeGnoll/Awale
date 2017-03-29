import numpy
from main import can_play


def get_state(board, player):
    board = numpy.copy(board)
    if player == 1:
        board = numpy.array([board[(i + 6) % 12] for i in range(12)])

    state = -numpy.ones(32 * 12)
    for i in range(12):
        for j in range(board[i]):
            state[i * 32 + j] = 1

    return state


def get_move(state, model):
    [q_values] = model.predict(numpy.array([state]))
    return numpy.argmax(q_values)


class QPlayer:
    def __init__(self, model):
        self.model = model

    def get_move(self, awale, player):
        board = awale.board
        score = awale.score
        state = get_state(board, player)
        move = get_move(state, self.model) + 6 * player

        if can_play(board, score, player, move):
            return move
        else:
            raise ValueError("Erreur! La case {} ne peut pas être jouée.".format(move))
