import numpy
import random

from awale_fun import init_board, will_starve, can_play, play, get_winner
from q_player import get_state, get_move, reverse_board
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop
from collections import deque

def init_model():
    model = Sequential()
    model.add(Dense(512, init='lecun_uniform', input_shape=(48 * 12,)))
    model.add(Activation('relu'))

    model.add(Dense(512, init='lecun_uniform'))
    model.add(Activation('relu'))

    model.add(Dense(512, init='lecun_uniform'))
    model.add(Activation('relu'))

    model.add(Dense(6, init='lecun_uniform'))
    model.add(Activation('linear'))

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    return model

# def init_model():
#     """
#     Init model
#     :return: model
#     """
#
#     model = Sequential()
#
#     model.add(Dense(512, input_dim=48 * 12, kernel_initializer="lecun_uniform"))
#     model.add(Activation('relu'))
#
#     model.add(Dense(512, kernel_initializer="lecun_uniform"))
#     model.add(Activation('relu'))
#
#     model.add(Dense(512, kernel_initializer="lecun_uniform"))
#     model.add(Activation('relu'))
#
#     model.add(Dense(512, kernel_initializer="lecun_uniform"))
#     model.add(Activation('relu'))
#
#     model.add(Dense(6, kernel_initializer="lecun_uniform"))
#     model.add(Activation('linear'))
#
#     rms = RMSprop()
#     model.compile(loss='mse', optimizer=rms)
#
#     return model

model = init_model()

epochs = 1000
gamma = 0.99
epsilon = 0.1
batch_size = 256
buffer = 8196
replay = deque()

losses = []
winners = []
scores = []
moves_counts = []

erreurs_case_vide = 0
erreurs_famine = 0

for epoch in range(epochs):
    if epoch % 100 == 0 and epoch != 0:
        print("epoch = {}".format(epoch))

    # Experience replay
    loss = -1
    if len(replay) > batch_size:
        batch = random.sample(replay, batch_size)

        X = numpy.zeros((batch_size, 48 * 12))
        Y = numpy.zeros((batch_size, 6))

        old_states = numpy.array([b[0] for b in batch])
        new_states = numpy.array([b[2] for b in batch])

        old_q_values = model.predict(old_states)
        new_q_values = model.predict(new_states)

        for i in range(batch_size):
            _, move, _, reward, terminal = batch[i]

            if terminal:
                update = reward
            else:
                update = reward - gamma * max(new_q_values[i])

            old_q_values[i][move] = update

            X[i] = old_states[i]
            Y[i] = old_q_values[i]

        loss = model.train_on_batch(X, Y)

    losses.append(loss)

    # Initialisation environnement
    moves_count = 0
    max_count = 400
    board = init_board()
    score = 0
    winner = -2

    reward = None

    # Lancement de la partie
    while winner == -2 and moves_count < max_count:
        moves_count += 1

        state = get_state(board)

        # Calcul du coup à jouer
        if random.random() < epsilon:
            moves = []

            for i in range(6):
                if can_play(board, [0, 0], 0, i):
                    moves.append(i)

            move = random.choice(moves)
        else:
            move = get_move(state, model)

        if can_play(board, [0, 0], 0, move):
            board, [delta_score, _] = play(board, [0, 0], 0, move)
            score += delta_score
            winner = get_winner(board, [score / 2, score / 2], winner, 0)
        else:
            delta_score = 0
            if board[move] == 0:
                erreurs_case_vide += 1
            elif will_starve(board, [0, 0], 0, move):
                erreurs_famine += 1
            winner = -3

        winners.append(winner)

        reward = {-3: -24, -2: delta_score, -1: 0, 0: 0, 1: 0}[winner]
        new_state = get_state(board)
        terminal = winner != -2

        if len(replay) == buffer:
            replay.popleft()
        replay.append((state, move, new_state, reward, terminal))

        board = reverse_board(board)

    scores.append(score)
    moves_counts.append(moves_count)

    if moves_count >= max_count:
        print("La partie est trop longue (plus de 400 coups).")

filename = "C:\\Users\\Laouen\\PycharmProjects\\Awale\\QPlayers\\qplayer_epochs{}_gamma{}_epsilon{}.model".format(
    epochs, gamma, epsilon)
model.save(filename)

losses = numpy.array(losses)
losses = losses[losses != -1]
winners = numpy.array(winners)
winners = winners[winners != -2]

numpy.save(
    "C:\\Users\\Laouen\\PycharmProjects\\Awale\\TableauxQ-learning\\losses_epochs{}_gamma{}_epsilon{}.npy".format(
        epochs, gamma, epsilon),
    losses)
numpy.save(
    "C:\\Users\\Laouen\\PycharmProjects\\Awale\\TableauxQ-learning\\winners_epochs{}_gamma{}_epsilon{}.npy".format(
        epochs, gamma, epsilon),
    winners)
numpy.save(
    "C:\\Users\\Laouen\\PycharmProjects\\Awale\\TableauxQ-learning\\score0_epochs{}_gamma{}_epsilon{}.npy".format(
        epochs, gamma, epsilon),
    scores)

print("case vide = {}".format(erreurs_case_vide))
print("famine = {}".format(erreurs_famine))


import matplotlib.pyplot as plt
plt.subplot(221)
plt.plot(range(len(losses)), losses)
plt.subplot(222)
plt.plot(range(len(moves_counts)), moves_counts)
plt.subplot(223)
plt.plot(range(len(scores)), scores)
plt.show()