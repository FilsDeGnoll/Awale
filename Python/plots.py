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

score.set_title("Score moyen")
score.set_xlabel("époque")
score.set_ylabel("score")

winner.set_title("Gagnant")
winner.set_xlabel("époque")
winner.set_ylabel("pourcentage")
winner.set_ybound(0, 100)

labels = ["QPlayer", "Adversaire", "Erreur"]
markers = ["v", "o", "P"]
colors = ["black", "black", "black"]
lines = []
for i in range(len(colors)):
    lines.append(mlines.Line2D([], [], color=colors[i], label=labels[i], marker=markers[i]))
winner.legend(handles=lines)

names = ["gamma = ", "gamma = ", "gamma = "]
colors = ["blue", "green", "red"]
lines = []
for i in range(len(names)):
    lines.append(mlines.Line2D([], [], color=colors[i], label=names[i], marker="o"))
legend.remove()
l = [names[i] for i in range(len(names))]
legend = fig.legend(lines, l, 'lower right')

epochs = 50000
gamma = 0.75
n = epochs // 25
x = [i * n for i in range(25)]
winner0 = numpy.zeros(25)
winner1 = numpy.zeros(25)
error = numpy.zeros(25)

winners = numpy.load(
    "C:\\Users\\Laouen\\PycharmProjects\\Awale\\Tableaux\ Q-learning\\winners_e{}_g{}.npy".format(epochs, gamma))
loss = numpy.load(
    "C:\\Users\\Laouen\\PycharmProjects\\Awale\\Tableaux\ Q-learning\\loss_e{}_g{}.npy".format(epochs, gamma))
score0 = numpy.load(
    "C:\\Users\\Laouen\\PycharmProjects\\Awale\\Tableaux\ Q-learning\\score0_e{}_g{}.npy".format(epochs, gamma))
score1 = numpy.load(
    "C:\\Users\\Laouen\\PycharmProjects\\Awale\\Tableaux\ Q-learning\\score1_e{}_g{}.npy".format(epochs, gamma))

for i in range(25):
    w = winners[i * n:(i + 1) * n]
    winner0[i] = sum(w == 0) * 100 / n
    winner1[i] = sum(w == 1) * 100 / n
    error[i] = sum(w == -3) * 100 / n

loss.plot(x, [numpy.array(loss[i * n:(i + 1) * n]).mean() for i in range(25)], "-v")

winner.plot(x, winner0, "-v")
winner.plot(x, winner1, "-o")
winner.plot(x, error, "-P")

score.plot(x, [numpy.array(score0[i * n:(i + 1) * n]).mean() for i in range(25)], "-v", color="blue")
score.plot(x, [numpy.array(score1[i * n:(i + 1) * n]).mean() for i in range(25)], "-o", color="green")

plt.show()
