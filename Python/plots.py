import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy

width = 100
height = 100

fig = plt.figure()
loss = fig.add_subplot(221)
winner = fig.add_subplot(222)
score = fig.add_subplot(223)
legend = fig.legend([], [], 'lower right')
fig.set_tight_layout(True)

loss.set_title("Perte")
loss.set_xlabel("époque")
loss.set_ylabel("perte")

winner.set_title("Gagnant")
winner.set_xlabel("époque")
winner.set_ylabel("pourcentage")
winner.set_ybound(0, 100)

score.set_title("Score moyen")
score.set_xlabel("époque")
score.set_ylabel("score")

labels = ["QPlayer", "Adversaire", "Erreur"]
markers = ["v", "o", "P"]
colors = ["black", "black", "black"]
lines = []
for i in range(len(labels)):
    lines.append(mlines.Line2D([], [], color=colors[i], label=labels[i], marker=markers[i]))
winner.legend(handles=lines)

labels = ["QPlayer", "Adversaire"]
markers = ["v", "o"]
colors = ["black", "black"]
lines = []
for i in range(len(labels)):
    lines.append(mlines.Line2D([], [], color=colors[i], label=labels[i], marker=markers[i]))
score.legend(handles=lines)

names = ["gamma = 0.2", "gamma = 0.5", "gamma = 0.8"]
colors = ["blue", "green", "red"]
lines = []
for i in range(len(names)):
    lines.append(mlines.Line2D([], [], color=colors[i], label=names[i], marker="o"))
legend.remove()
l = [names[i] for i in range(len(names))]
legend = fig.legend(lines, l, 'lower right')

epochs = 10000
gamma = [0.2, 0.5, 0.8]
n = epochs // 25
x = [i * n for i in range(25)]
winner0 = numpy.zeros(25)
winner1 = numpy.zeros(25)
error = numpy.zeros(25)

for i in range(len(gamma)):
    winners = numpy.load(
        "C:\\Users\\Laouen\\PycharmProjects\\Awale\\TableauxQ-learning\\winners_e{}_g{}.npy".format(epochs, gamma[i]))
    losses = numpy.load(
        "C:\\Users\\Laouen\\PycharmProjects\\Awale\\TableauxQ-learning\\losses_e{}_g{}.npy".format(epochs, gamma[i]))
    score0 = numpy.load(
        "C:\\Users\\Laouen\\PycharmProjects\\Awale\\TableauxQ-learning\\score0_e{}_g{}.npy".format(epochs, gamma[i]))
    score1 = numpy.load(
        "C:\\Users\\Laouen\\PycharmProjects\\Awale\\TableauxQ-learning\\score1_e{}_g{}.npy".format(epochs, gamma[i]))

    for j in range(25):
        w = winners[j * n:(j + 1) * n]
        winner0[j] = sum(w == 0) * 100 / n
        winner1[j] = sum(w == 1) * 100 / n
        error[j] = sum(w == -3) * 100 / n

    loss.plot(x, [numpy.array(losses[j * n:(j + 1) * n]).mean() for j in range(25)], "-v", color=colors[i])

    winner.plot(x, winner0, "-v", color=colors[i])
    winner.plot(x, winner1, "-o", color=colors[i])
    winner.plot(x, error, "-P", color=colors[i])

    score.plot(x, [numpy.array(score0[j * n:(j + 1) * n]).mean() for j in range(25)], "-v", color=colors[i])
    score.plot(x, [numpy.array(score1[j * n:(j + 1) * n]).mean() for j in range(25)], "-o", color=colors[i])

plt.show()
