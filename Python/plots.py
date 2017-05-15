import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy

fig = plt.figure()
loss = fig.add_subplot(221)
epsilon = fig.add_subplot(222)
winner = fig.add_subplot(223)
score = fig.add_subplot(224)
legend = fig.legend([], [], 'lower right')
fig.set_tight_layout(True)

loss.set_title("Perte")
loss.set_xlabel("époque")
loss.set_ylabel("perte")

epsilon.set_title("Epsilon")
epsilon.set_xlabel("époque")
epsilon.set_ylabel("epsilon")

winner.set_title("Gagnant")
winner.set_xlabel("époque")
winner.set_ylabel("pourcentage")
winner.set_ybound(0, 100)

score.set_title("Score moyen")
score.set_xlabel("époque")
score.set_ylabel("score")

opponent = "NegabetaPlayer_depth3_eval2"
labels = ["QPlayer", opponent, "Erreur"]
markers = ["v", "o", "P"]
colors = ["black", "black", "black"]
lines = []
for i in range(len(labels)):
    lines.append(mlines.Line2D([], [], color=colors[i], label=labels[i], marker=markers[i]))
winner.legend(handles=lines)

labels = ["QPlayer", opponent]
markers = ["v", "o"]
colors = ["black", "black"]
lines = []
for i in range(len(labels)):
    lines.append(mlines.Line2D([], [], color=colors[i], label=labels[i], marker=markers[i]))
score.legend(handles=lines)

names = ["gamma = 0.99"]
colors = ["blue", "green", "red"]
lines = []
for i in range(len(names)):
    lines.append(mlines.Line2D([], [], color=colors[i], label=names[i], marker="o"))
legend.remove()
l = [names[i] for i in range(len(names))]
legend = fig.legend(lines, l, 'lower right')

exploration_epochs = 15000
exploitation_epochs = 5000
epochs = exploration_epochs + exploitation_epochs
gamma = [0.99]
n = epochs // 25
x = [i * n for i in range(25)]
winner0 = numpy.zeros(25)
winner1 = numpy.zeros(25)
error = numpy.zeros(25)

for i in range(len(gamma)):
    losses = numpy.load(
        "C:\\Users\\Laouen\\PycharmProjects\\Awale\\TableauxQ-learning\\losses_exploration_epochs{}_exploitation_epochs{}_gamma{}_opponent{}.npy".format(
            exploration_epochs, exploitation_epochs, gamma[i], opponent))
    epsilons = numpy.load(
        "C:\\Users\\Laouen\\PycharmProjects\\Awale\\TableauxQ-learning\\epsilons_exploration_epochs{}_exploitation_epochs{}_gamma{}_opponent{}.npy".format(
            exploration_epochs, exploitation_epochs, gamma[i], opponent))
    winners = numpy.load(
        "C:\\Users\\Laouen\\PycharmProjects\\Awale\\TableauxQ-learning\\winners_exploration_epochs{}_exploitation_epochs{}_gamma{}_opponent{}.npy".format(
            exploration_epochs, exploitation_epochs, gamma[i], opponent))
    score0 = numpy.load(
        "C:\\Users\\Laouen\\PycharmProjects\\Awale\\TableauxQ-learning\\score0_exploration_epochs{}_exploitation_epochs{}_gamma{}_opponent{}.npy".format(
            exploration_epochs, exploitation_epochs, gamma[i], opponent))
    score1 = numpy.load(
        "C:\\Users\\Laouen\\PycharmProjects\\Awale\\TableauxQ-learning\\score1_exploration_epochs{}_exploitation_epochs{}_gamma{}_opponent{}.npy".format(
            exploration_epochs, exploitation_epochs, gamma[i], opponent))

    for j in range(25):
        w = winners[j * n:(j + 1) * n]
        winner0[j] = sum(w == 0) * 100 / n
        winner1[j] = sum(w == 1) * 100 / n
        error[j] = sum(w == -3) * 100 / n

    p = len(losses) // 25

    loss.plot(x, [numpy.array(losses[j * p:(j + 1) * p]).mean() for j in range(25)], "-v", color=colors[i])

    epsilon.plot(x, [numpy.array(epsilons[j * p:(j + 1) * p]).mean() for j in range(25)], "-v", color=colors[i])

    winner.plot(x, winner0, "-v", color=colors[i])
    winner.plot(x, winner1, "-o", color=colors[i])
    winner.plot(x, error, "-P", color=colors[i])

    score.plot(x, [numpy.array(score0[j * n:(j + 1) * n]).mean() for j in range(25)], "-v", color=colors[i])
    score.plot(x, [numpy.array(score1[j * n:(j + 1) * n]).mean() for j in range(25)], "-o", color=colors[i])

plt.show()
