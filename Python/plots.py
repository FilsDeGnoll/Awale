import matplotlib.pyplot as plt
import numpy

colors = {5000 : "Représentation 2", 4999 : "Représentation 1", 4998 : "NewbiePlayer"}
for epoch in [5000, 4999, 4998]:
    losses = numpy.load("C:\\Users\\Laouen\\PycharmProjects\\Awale\\Tableaux-Q-learning\\losses_epochs{}_gamma0.9_epsilon0.1.npy".format(epoch))
    scores = numpy.load("C:\\Users\\Laouen\\PycharmProjects\\Awale\\Tableaux-Q-learning\\scores_epochs{}_gamma0.9_epsilon0.1.npy".format(epoch))
    moves_counts = numpy.load("C:\\Users\\Laouen\\PycharmProjects\\Awale\\Tableaux-Q-learning\\moves_counts_epochs{}_gamma0.9_epsilon0.1.npy".format(epoch))

    epochs = 5000
    n = epochs // 25
    x = [i * n for i in range(25)]

    # plt.subplot(221)
    # p = len(losses) // 25
    # plt.plot(x, [numpy.array(losses[i * p:(i + 1) * p]).mean() for i in range(25)], label=colors[epoch])
    # plt.legend()
    # plt.xlabel("Époque")
    # plt.ylabel("Perte")
    # plt.subplot(222)
    # plt.plot(x, [numpy.array(scores[i * n:(i + 1) * n]).mean() for i in range(25)], label=colors[epoch])
    # plt.legend()
    # plt.xlabel("Époque")
    # plt.ylabel("Score moyen")
    # plt.subplot(223)
    plt.plot(x, [numpy.array(moves_counts[i * n:(i + 1) * n]).mean() for i in range(25)], label=colors[epoch], linewidth=2)
    plt.legend()
    plt.xlabel("Époque", size=16)
    plt.ylabel("Nombre de coups moyen", size=16)
    plt.tight_layout()
    plt.xticks(size=14)
    plt.yticks(size=14)
plt.show()