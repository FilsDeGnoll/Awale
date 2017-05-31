import numpy
import random

from datetime import datetime
from awale_fun import *
from awale_oop import Awale
from newbie_player import NewbiePlayer
from q_player import *
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop
from collections import deque

def init_model():
    """
    Init model
    :return: model
    """

    model = Sequential()

    model.add(Dense(512, input_dim=48 * 12, init="lecun_uniform"))
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

epochs = 1000
gamma = 0.9
epsilon = 0.1
batch_size = 256
memory_size = 8196
memory = deque()
get_state = get_state1

losses = []
winners = []
scores = []
moves_counts = []

for epoch in range(epochs):
    if epoch % 100 == 0:
        print("epoch = {}".format(epoch))

    # Experience replay
    loss = -1
    if len(memory) > batch_size:
        batch = random.sample(memory, batch_size)

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
    player = 0

    reward = None

    # Lancement de la partie
    while winner == -2 and moves_count < max_count:
        moves_count += 1

        state = get_state(board)

        # Calcul du coup à jouer
        if player == 1:
            move = NewbiePlayer().get_move(Awale(board), 0)
        elif random.random() < epsilon:
            move = get_random_move(board, player)
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
        if player == 0:
            memory.append((state, move, new_state, reward, terminal))

        board = reverse_board(board)
        player = 1 - player

        winners.append(winner)

    scores.append(score)
    moves_counts.append(moves_count)

    if moves_count >= max_count:
        print("La partie est trop longue (plus de 400 coups).")

date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
parameters = "-gamma-{}-epsilon-{}-epochs{}-".format(gamma, epsilon, epochs)

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
    numpy.save(filename,arrays[i])