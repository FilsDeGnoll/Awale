import random
from collections import deque
from datetime import datetime

import numpy
from keras.layers.core import Dense, Activation
from keras.models import Sequential
from keras.optimizers import RMSprop

from awale_fun import init_board, get_random_move, can_play, play, get_winner
from q_player import get_state, get_move, reverse_board


def init_model():
    """
    Init model
    :return: model
    """

    model = Sequential()

    model.add(Dense(512, input_dim=12 * 48, init="lecun_uniform"))
    model.add(Activation('relu'))

    model.add(Dense(512, init="lecun_uniform"))
    model.add(Activation('relu'))

    model.add(Dense(512, init="lecun_uniform"))
    model.add(Activation('relu'))

    model.add(Dense(512, init="lecun_uniform"))
    model.add(Activation('relu'))

    model.add(Dense(6, init="lecun_uniform"))
    model.add(Activation('linear'))

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    return model


model = init_model()

# Paramètres de l'entraînement
epochs = 10000
gamma = 0.9
epsilon = 0.1
batch_size = 512
memory_size = 25000
memory = deque()

losses = []
winners = []
scores = []
moves_counts = []

# Lancement de l'entraînement
for epoch in range(epochs):
    if epoch % 100 == 0:
        print("epoch = {}".format(epoch))

    # Experience replay
    loss = -1
    if len(memory) > batch_size:
        batch = random.sample(memory, batch_size)

        X = numpy.zeros((batch_size, 12 * 48))
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

    # Initialisation de l'environnement
    moves_count = 0
    max_count = 1000
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
            move = get_random_move(board, 0)
        else:
            move = get_move(state, model)

        # Le coup est joué
        if can_play(board, 0, move):
            board, [delta_score, _] = play(board, [0, 0], 0, move)
            score += delta_score
            winner = get_winner(board, [score / 2, score / 2], winner, 0)
        else:
            delta_score = 0
            winner = -3

        # Sauvegarde dans la mémoire
        reward = {-3: -24, -2: delta_score, -1: 0, 0: 0, 1: 0}[winner]
        new_state = get_state(board)
        terminal = winner != -2

        if len(memory) == memory_size:
            memory.popleft()
        memory.append((state, move, new_state, reward, terminal))

        # Renversement du plateau
        board = reverse_board(board)

        winners.append(winner)

    scores.append(score)
    moves_counts.append(moves_count)

    if moves_count >= max_count:
        print("La partie est trop longue (plus de {} coups).".format(max_count))

date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
parameters = "-gamma-{}-epsilon-{}-epochs-{}-".format(gamma, epsilon, epochs)

directory = "C:\\Users\\Laouen\\PycharmProjects\\Awale\\QPlayers\\"
filename = directory + "qplayer" + parameters + date + ".model"
model.save(filename)

losses = numpy.array(losses)
losses = losses[losses != -1]
winners = numpy.array(winners)
winners = winners[winners != -2]

directory = "C:\\Users\\Laouen\\PycharmProjects\\Awale\\Tableaux-Q-learning\\"
arrays = [losses, winners, scores, moves_counts]
names = ["losses", "winners", "scores", "moves_counts"]

for i in range(len(arrays)):
    filename = directory + names[i] + parameters + date + ".npy"
    numpy.save(filename, arrays[i])
