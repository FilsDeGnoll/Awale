import matplotlib.pyplot as plt
import numpy

# directory = "C:\\Users\\Laouen\\PycharmProjects\\Awale\\Tableaux-Q-learning\\"
# names = ["losses", "scores", "moves_counts"]
# ylabels = ["Perte", "Score moyen", "Nombre de coups moyen"]
#
# gamma = 0.9
# epsilon = 0.1
# epochs = 35000
# n = epochs // 25
# x = [i * n for i in range(25)]
#
# parameters = "-gamma-{}-epsilon-{}-epochs-{}-".format(gamma, epsilon, epochs)
# date = "2017-06-10-18-35-43"
#
# for i in range(len(names)):
#     filename = filename = directory + names[i] + parameters + date + ".npy"
#     array = numpy.load(filename)
#     p = len(array) // 25
#
#     # plt.figure(dpi=180)
#     plt.plot(x, [numpy.array(array[j * p:(j + 1) * p]).mean() for j in range(25)], "-o", linewidth=2)
#     plt.title(ylabels[i] + " en fonction du nombre de parties jouées", size=18)
#     plt.xlabel("Nombre de parties jouées", size=16)
#     plt.ylabel(ylabels[i], size=16)
#     plt.xticks(size=14)
#     plt.yticks(size=14)
#
#     plt.show()

directory = "C:\\Users\\Laouen\\PycharmProjects\\Awale\\Tableaux-Q-learning\\"

gamma = 0.9
epsilon = 0.1
epochs = 35000
n = epochs // 25
x = [i * n for i in range(25)]

parameters = "-gamma-{}-epsilon-{}-epochs-{}-".format(gamma, epsilon, epochs)
date = "2017-06-10-18-35-43"
filename = filename = directory + "moves_counts" + parameters + date + ".npy"

array = numpy.load(filename)
p = len(array) // 25
plt.plot(x, [numpy.array(array[j * p:(j + 1) * p]).mean() for j in range(25)], "-o", linewidth=2, label="epsilon = 0.1")

gamma = 0.5
parameters = "-gamma-{}-epsilon-{}-epochs-{}-".format(gamma, epsilon, epochs)
# date = "2017-06-11-17-03-49"
filename = filename = directory + "moves_counts" + parameters + date + ".npy"

array = numpy.load(filename)
p = len(array) // 25
plt.plot(x, [numpy.array(array[j * p:(j + 1) * p]).mean() for j in range(25)], "-o", linewidth=2, label="epsilon = 0.5")

gamma = 0.9
parameters = "-gamma-{}-epsilon-{}-epochs-{}-".format(gamma, epsilon, epochs)
# date = "2017-06-11-18-48-00"
filename = filename = directory + "moves_counts" + parameters + date + ".npy"

array = numpy.load(filename)
p = len(array) // 25
plt.plot(x, [numpy.array(array[j * p:(j + 1) * p]).mean() for j in range(25)], "-o", linewidth=2, label="epsilon = 0.9")

plt.legend()
plt.show()