import numpy
import random
from awale_oop import Awale
from negabeta_player import NegabetaPlayer
from q_player import get_state
from evaluation import evaluation2
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop


def init_model():
    model = Sequential()
    model.add(Dense(512, init='lecun_uniform', input_shape=(32 * 12,)))
    model.add(Activation('relu'))

    model.add(Dense(512, init='lecun_uniform'))
    model.add(Activation('relu'))

    model.add(Dense(6, init='lecun_uniform'))
    model.add(Activation('tanh'))

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    return model


model = init_model()

n = 0

while n < 10000:
    print(n)
    awale = Awale()
    players = [NegabetaPlayer(5, evaluation2), NegabetaPlayer(4, evaluation2)]
    moves_count = 0
    max_count = 400
    player = 0

    while awale.winner == -2 and moves_count < max_count:
        moves_count += 1

        if random.random() < 0.2:
            moves = []
            minmove = player * 6
            maxmove = (1 + player) * 6
            for i in range(minmove, maxmove):
                if awale.can_play(player, i):
                    moves.append(i)
            move = random.choice(moves)
        else:
            move = players[player].get_move(awale, player)
            if random.random() < 0.1:
                n += 1
                state = get_state(awale.board, player)
                q_values = numpy.zeros(6)
                q_values[move - player * 6] = 1
                X = numpy.array([state])
                Y = numpy.array([q_values])
                model.train_on_batch(X, Y)

        if awale.can_play(player, move):
            awale.play(player, move)
            awale.check_winner(player)
        else:
            raise ValueError("Erreur! La case {} ne peut pas être jouée.".format(move))

        player = 1 - player

filename = "C:\\Users\\Laouen\\PycharmProjects\\Awale\\QPlayers\\qplayer_n{}.model".format(n)
model.save(filename)
