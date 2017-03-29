# Basé sur le tutoriel http://outlace.com/Reinforcement-Learning-Part-3/
import numpy
import random
from awale import Awale
from main import init_board, play, can_play, get_winner
from random_player import RandomPlayer
from newbie_player import NewbiePlayer
from q_player import get_state, get_move
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
    model.add(Activation('linear'))

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    return model


exploration_epochs = 45000
final_epochs = 5000
epochs = exploration_epochs + final_epochs
gamma = 0.75
initial_epsilon = 0.75
final_epsilon = 1e-5
epsilon = initial_epsilon

loss = []
winners = []
score0 = []
score1 = []

model = init_model()

for epoch in range(epochs):
    if epoch % 100 == 0 and epoch != 0:
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

    old_state, old_move, reward = None, None, None

    while winner == -2 and moves_count < max_count:
        moves_count += 1

        if player == 0:
            state = get_state(board, player)

            if random.random() < epsilon:
                move = numpy.random.randint(6)
            else:
                move = get_move(state, model)

            old_state, old_move = state, move
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
            reward = {-3: -100, -2: delta_score[0] - delta_score[1], -1: 0, 0: 0, 1: 0}[winner]

        if player == 1 or winner != -2:
            [old_q_values] = model.predict([numpy.array([old_state])])

            if winner == -2:
                new_state = get_state(board, 0)
                [new_q_values] = model.predict([numpy.array([new_state])])
                old_q_values[old_move] = reward + gamma * max(new_q_values)
            else:
                old_q_values[old_move] = reward

            X = numpy.array([old_state])
            Y = numpy.array([old_q_values])
            l = model.train_on_batch(X, Y)
            loss.append(l)

        player = 1 - player

    score0.append(score[0])
    score1.append(score[1])

    if moves_count >= max_count:
        print("La partie est trop longue.")

filename = "qplayer_e{}_g{}.model".format(epochs, gamma)
model.save(filename)

winners = numpy.array(winners)
winners = winners[winners != -2]

numpy.save("C:\\Users\\Laouen\\PycharmProjects\\Awale\\Tableaux\ Q-learning\\winners_e{}_g{}.npy".format(epochs, gamma),
           winners)
numpy.save("C:\\Users\\Laouen\\PycharmProjects\\Awale\\Tableaux\ Q-learning\\loss_e{}_g{}.npy".format(epochs, gamma),
           loss)
numpy.save("C:\\Users\\Laouen\\PycharmProjects\\Awale\\Tableaux\ Q-learning\\score0_e{}_g{}.npy".format(epochs, gamma),
           score0)
numpy.save("C:\\Users\\Laouen\\PycharmProjects\\Awale\\Tableaux\ Q-learning\\score1_e{}_g{}.npy".format(epochs, gamma),
           score1)
