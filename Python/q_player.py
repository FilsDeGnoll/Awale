import numpy
from Python.awale_fun import can_play

def reverse_board(board):
    return numpy.array([board[(i + 6) % 12] for i in range(12)])

# def get_state(board):
#     state = -numpy.ones(32 * 12)
#     for i in range(12):
#         for j in range(board[i]):
#             state[i * 32 + j] = 1
#         if board[i] >= 32:
#             print("plus de 32 graines")
#
#     return state

def get_state(board):
    """
    Return features of board
    :param board: board
    :return: features
    """

    t = -numpy.ones((12, 48))

    t[numpy.arange(12), board.T] = 1

    return t.flatten()


def get_move(state, model):
    [q_values] = model.predict(numpy.array([state]))

    return numpy.argmax(q_values)


class QPlayer:
    def __init__(self, model):
        self.model = model

    def get_move(self, awale, player):
        board = awale.board
        score = awale.score
        if player == 1:
            board = reverse_board(board)

        state = get_state(board)
        move = get_move(state, self.model) + 6 * player

        if can_play(board, score, player, move):
            return move
        else:
            raise ValueError("Erreur! La case {} ne peut pas être jouée.".format(move))
