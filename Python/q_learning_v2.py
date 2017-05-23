import numpy
import random
from awale_fun import init_board, will_starve, can_play, play, get_winner
from q_player import get_state, get_move
from keras.models import load_model

n = 10007
model = load_model("C:\\Users\\Laouen\\PycharmProjects\\Awale\\QPlayers\\qplayer_n{}.model".format(n))

epochs = 10000
gamma = 0.99
epsilon = 0.1

losses = []
winners = []
score0 = []
score1 = []

erreurs_case_vide = 0
erreurs_famine = 0

for epoch in range(epochs):
    if epoch % 100 == 0 and epoch != 0:
        print("epoch = {}".format(epoch))

    moves_count = 0
    max_count = 400
    board = init_board()
    score = [0, 0]
    winner = -2
    player = 0

    old_state, old_move, reward = None, None, None

    while winner == -2 and moves_count < max_count:
        moves_count += 1

        state = get_state(board, player)

        if random.random() < epsilon:
            moves = []
            minmove = player * 6
            maxmove = (1 + player) * 6

            for i in range(minmove, maxmove):
                if can_play(board, score, player, i):
                    moves.append(i)
            move = random.choice(moves)
        else:
            move = get_move(state, model)

        old_state, old_move = state, move

        if can_play(board, score, player, move):
            board, new_score = play(board, score, player, move)
            delta_score = [new_score[i] - score[i] for i in range(2)]
            score = new_score
            winner = get_winner(board, score, winner, player)
        else:
            if board[move] == 0:
                erreurs_case_vide += 1
            elif will_starve(board, score, player, move):
                erreurs_famine += 1
            winner = -3

        winners.append(winner)

        reward = {-3: -1, -2: int(delta_score[0] - delta_score[1] > 0), -1: 0, 0: 0, 1: 0}[winner]

        [old_q_values] = model.predict([numpy.array([old_state])])

        if winner == -2:
            new_state = get_state(board, player)
            [new_q_values] = model.predict(numpy.array([new_state]))
            old_q_values[old_move - player * 6] = reward - gamma * max(new_q_values)
        else:
            old_q_values[old_move] = reward

        X = numpy.array([old_state])
        Y = numpy.array([old_q_values])
        loss = model.train_on_batch(X, Y)
        losses.append(loss)

        player = 1 - player

    score0.append(score[0])
    score1.append(score[1])

    if moves_count >= max_count:
        print("La partie est trop longue (plus de 400 coups).")

filename = "C:\\Users\\Laouen\\PycharmProjects\\Awale\\QPlayers\\qplayer_epochs{}_gamma{}_epsilon{}.model".format(
    epochs, gamma, epsilon)
model.save(filename)

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
    score0)
numpy.save(
    "C:\\Users\\Laouen\\PycharmProjects\\Awale\\TableauxQ-learning\\score1_epochs{}_gamma{}_epsilon{}.npy".format(
        epochs, gamma, epsilon),
    score1)

print("case vide = {}".format(erreurs_case_vide))
print("famine = {}".format(erreurs_famine))
