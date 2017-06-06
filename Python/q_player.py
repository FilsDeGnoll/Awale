import numpy
from awale_fun import can_play

def reverse_board(board):
    return numpy.array([board[(i + 6) % 12] for i in range(12)])

def get_state1(board):
    state = -numpy.ones(48 * 12)
    for i in range(12):
        for j in range(board[i]):
            state[i * 48 + j] = 1

    return state

def get_state2(board):
    state = -numpy.ones((12, 48))

    state[numpy.arange(12), board.T] = 1

    return state.flatten()


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
            r_board = reverse_board(board)
        else:
            r_board = board

        state = get_state2(r_board)
        move = get_move(state, self.model) + 6 * player

        if can_play(board, player, move):
            return move
        else:
            raise ValueError("Erreur! La case {} ne peut pas être jouée.".format(move))
