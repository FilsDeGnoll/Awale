import matplotlib.pyplot as plt
import numpy


directory = "C:\\Users\\Laouen\\PycharmProjects\\Awale\\Tableaux-Q-learning\\"
names = ["losses", "scores", "moves_counts"]
ylabels = ["Perte", "Score moyen", "Nombre de coups moyen pour finir une partie"]

gamma = 0.9
epsilon = 0.1
epochs = 20000
n = epochs // 25
x = [i * n for i in range(25)]

parameters = "-gamma-{}-epsilon-{}-epochs-{}-".format(gamma, epsilon, epochs)
date = "2017-06-03-16-52-32"

for i in range(len(names)):
    filename = filename = directory + names[i] + parameters + date + ".npy"
    array = numpy.load(filename)
    p = len(array) // 25

    plt.plot(x, [numpy.array(array[j * p:(j + 1) * p]).mean() for j in range(25)], "-o", linewidth=2)
    plt.title(ylabels[i] + " en fonction du nombre de parties jouées", size=18)
    plt.xlabel("Nombre de parties jouées", size=16)
    plt.ylabel(ylabels[i], size=16)
    plt.xticks(size=14)
    plt.yticks(size=14)

    plt.show()

filename = directory + "winners" + parameters + date + ".npy"
winners = numpy.load(filename)
qplayer_win = numpy.zeros(25)

for i in range(25):
    w = winners[i * n:(i + 1) * n]
    qplayer_win[i] = sum(w == 0) * 100 / n

plt.plot(x, qplayer_win, "-o", linewidth=2)
plt.title("Pourcentage de victoire du modèle en fonction du nombre de parties jouées", size=18)
plt.xlabel("Nombre de parties", size=16)
plt.ylabel("Pourcentage de victoire du modèle", size=16)
plt.xticks(size=14)
plt.yticks(size=14)
plt.ylim(0, 100)

plt.show()