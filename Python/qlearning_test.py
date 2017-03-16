# Basé sur le tutoriel http://outlace.com/Reinforcement-Learning-Part-3/
import numpy
import random

from keras.callbacks import History

from awale import Awale
from game import Game
from human_player import HumanPlayer
from main import init_board, play, can_play, get_winner
from newbie_player import NewbiePlayer
from q_player import QPlayer
from random_player import RandomPlayer
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop
import matplotlib.pyplot as plt


def init_model():
    model = Sequential()
    model.add(Dense(512, init='lecun_uniform', input_shape=(48 * 12,)))
    model.add(Activation('relu'))

    model.add(Dense(512, init='lecun_uniform'))
    model.add(Activation('relu'))

    model.add(Dense(6, init='lecun_uniform'))
    model.add(Activation('linear'))  # linear output so we can have range of real-valued outputs

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    return model


def get_state(board, player):
    board = numpy.copy(board)
    if player == 1:
        board = numpy.array([board[(i + 6) % 12] for i in range(12)])

    state = -numpy.ones(48 * 12)
    for i in range(12):
        for j in range(board[i]):
            state[i * 48 + j] = 1
    return state


def get_moves(board, score, player):
    board = numpy.copy(board)
    minmove = player * 6
    maxmove = (1 + player) * 6
    moves = -numpy.ones(6)
    for i in range(minmove, maxmove):
        if can_play(board, score, player, i):
            moves[i] = 1
    return moves


def get_input_array(board, score, player):
    state = get_state(board, player)
    moves = get_moves(board, score, player)
    return state


def get_move(input_array, model):
    [q_values] = model.predict(numpy.array([input_array]))
    return numpy.argmax(q_values)


exploration_epochs = 9500
final_epochs = 500
epochs = exploration_epochs + final_epochs
gamma = 0.9
initial_epsilon = 0.75
final_epsilon = 0.01
epsilon = initial_epsilon

losses = []
winners = []
score0 = []
score1 = []
nbre_coups = []

model = init_model()

for epoch in range(epochs):
    if epoch % 100 == 0:
        print("epoch = {}".format(epoch))

    if epsilon > final_epsilon:
        epsilon -= (initial_epsilon - final_epsilon) / exploration_epochs
    else:
        epsilon = final_epsilon

    moves_count = 0
    max_count = 400
    board = init_board()
    score = [0, 0]
    winner = -2
    player = 0

    old_input_array, old_move, reward = None, None, None

    while winner == -2 and moves_count < max_count:
        moves_count += 1

        if player == 0:
            input_array = get_input_array(board, score, player)

            # Trouver le coup
            if random.random() < epsilon:
                move = numpy.random.randint(6)
            else:
                move = get_move(input_array, model)

            # Sauvegarder
            old_input_array, old_move = input_array, move
        else:
            move = RandomPlayer.get_move(Awale(board, score), player)

        if can_play(board, score, player, move):
            board, new_score = play(board, score, player, move)

            delta_score = [new_score[i] - score[i] for i in range(2)]
            score = new_score

            winner = get_winner(board, score, winner, player)
        else:
            winner = -3

        winners.append(winner)

        if player == 0:
            reward = {-3: -10, -2: 0 * (delta_score[0] - delta_score[1]), -1: -1, 0: 5, 1: -5}[winner]

        if player == 1 or winner != -2:
            [old_q_values] = model.predict([numpy.array([old_input_array])])

            if winner == -2:
                new_input_array = get_input_array(board, score, 0)
                [new_q_values] = model.predict([numpy.array([new_input_array])])

                old_q_values[old_move] = reward + gamma * max(new_q_values)
            else:
                old_q_values[old_move] = reward

            X = numpy.array([old_input_array])
            Y = numpy.array([old_q_values])
            loss = model.train_on_batch(X, Y)
            losses.append(loss)

        player = 1 - player
    score0.append(score[0])
    score1.append(score[1])
    nbre_coups.append(moves_count)
    if moves_count >= max_count:
        print("La partie est trop longue.")

# model.save("qlearner.model")

n = epochs // 25
x = [i * n for i in range(25)]

plt.subplot(221)
plt.plot(x, [numpy.array(losses[i * n:(i + 1) * n]).mean() for i in range(25)], "-o")
plt.xlabel("Époque")
plt.ylabel("Loss")

winner0 = numpy.zeros(25)
winner1 = numpy.zeros(25)
error = numpy.zeros(25)
winners = numpy.array(winners)

for i in range(25):
    w = winners[i * n:(i + 1) * n]
    p = sum(w != -2)
    winner0[i] = sum(w == 0) * 100 / p
    winner1[i] = sum(w == 1) * 100 / p
    error[i] = sum(w == -3) * 100 / p

plt.subplot(222)
plt.plot(x, winner0, "-o", label="Pourentage de parties gagnées par QPlayer", color="blue")
plt.plot(x, winner1, "-o", label="Pourentage de parties gagnées par NewbiePlayer", color="green")
plt.plot(x, error, "-o", label="Pourcentage de parties terminées pour coup invalide", color="red")
plt.xlabel("Époque")
plt.legend()

plt.subplot(223)
plt.plot(x, [numpy.array(score0[i * n:(i + 1) * n]).mean() for i in range(25)], "-o")
plt.xlabel("Époque")
plt.ylabel("Score moyen de QPlayer")

plt.subplot(224)
plt.plot(x, [numpy.array(score1[i * n:(i + 1) * n]).mean() for i in range(25)], "-o")
plt.xlabel("Époque")
plt.ylabel("Score moyen de RandomPlayer")
plt.show()
plt.plot(x, [numpy.array(nbre_coups[i * n:(i + 1) * n]).mean() for i in range(25)], "-o")
plt.show()

game = Game(QPlayer(model), RandomPlayer(), debug=True)
game.new_game()
game.display_result()
