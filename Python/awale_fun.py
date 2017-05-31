import numpy
from random import choice


def init_board():
    """
    Le plateau de jeu est constitué de 2 rangées de 6 trous, chaque trou contenant 4 graines au départ.
    """
    board = 4 * numpy.ones(12, numpy.int)

    return board


def deal(board, move):
    """
    Distribue les graines de la case indiquée et renvoie le nouveau plateau ainsi que l'indice de la case d'arrivée.
    :param board: plateau
    :param move: indice de la case à jouer
    :return: nouveau plateau, case d'arrivée
    """
    new_board = numpy.copy(board)
    seeds = new_board[move]
    new_board[move] = 0
    i = move

    while seeds > 0:
        i += 1

        if i % 12 != move:
            new_board[i % 12] += 1
            seeds -= 1

    return new_board, i % 12


def pick(board, score, player, move):
    """
    Ramasse les graines et renvoie le nouveau plateau ainsi que le nouveau score.
    :param board: plateau
    :param score: score
    :param player: numéro du joueur
    :param move: indice de la case à jouer
    :return: nouveau plateau, nouveau score
    """
    new_board, i = deal(board, move)
    new_score = score[:]
    minpick = (1 - player) * 6
    maxpick = (2 - player) * 6

    while minpick <= i < maxpick and 2 <= new_board[i] <= 3:
        new_score[player] += new_board[i]
        new_board[i] = 0

        i -= 1

    return new_board, new_score


def will_starve(board, player, move):
    """
    Vérifie si le joueur va affamer l'adversaire.
    :param board: plateau
    :param player: numéro du joueur
    :param move: indice de la case à jouer
    :return: "va affamer l'adversaire"
    """
    minpick = (1 - player) * 6
    maxpick = (2 - player) * 6
    new_board = pick(board, [0, 0], player, move)[0]
    starving = new_board[minpick:maxpick].sum() == 0

    return starving


def cannot_feed(board, player):
    """
    Vérifie si le joueur ne peut pas nourrir l'adversaire.
    :param board: plateau
    :param score: score
    :param player: numéro du joueur
    :return: "ne peut pas nourrir l'adversaire"
    """
    minmove = player * 6
    maxmove = (1 + player) * 6
    cannot_feed = True

    for i in range(minmove, maxmove):
        cannot_feed = cannot_feed and will_starve(board, player, i)

    return cannot_feed


def can_play(board, player, move):
    """
    Vérifie si le coup indiqué est valide.
    :param board: plateau
    :param score: score
    :param player: numéro du joueur
    :param move: indice de la case à jouer
    :return: "le coup est valide"
    """
    minmove = player * 6
    maxmove = (1 + player) * 6
    minpick = (1 - player) * 6
    maxpick = (2 - player) * 6

    if board[minpick:maxpick].sum() == 0:
        return minmove <= move < maxmove and board[move] != 0 and (
            not will_starve(board, player, move) or cannot_feed(board, player))
    else:
        return minmove <= move < maxmove and board[move] != 0


def play(board, score, player, move):
    """
    Joue le coup indiqué. Si le coup affame l'adversaire, le joueur ne ramasse pas les graines.
    :param player: numéro du joueur
    :param move: indice de la case à jouer
    :return: aucun retour
    """
    if will_starve(board, player, move):
        new_board = deal(board, move)[0]
        board = new_board
    else:
        board, score = pick(board, score, player, move)

    return board, score


def get_seeds(board, score):
    """
    Partage les graines s'il en reste sur le plateau à la fin de la partie : chaque joueur récupère les graines
    qui sont dans son territoire.
    :param board: plateau
    :param score: score
    :return: aucun retour
    """
    for i in range(12):
        if board[i] != 0:
            score[i // 6] += board[i]
            board[i] = 0


def get_winner(board, score, winner, player):
    """
    Vérifie si la partie est terminée : winner vaut -2 si la partie n'est pas terminée, -1 s'il y a égalité ou le numéro
    du gagnant sinon.
    :param board: plateau
    :param score: score
    :param winner: numéro du gagnant ou -2 si la partie n'est pas terminée
    :param player: numéro du joueur qui vient de jouer
    :return: nouvel état
    """
    if winner == -2:
        minpick = (1 - player) * 6
        maxpick = (2 - player) * 6
        if board[minpick:maxpick].sum() == 0 or score[player] >= 24:
            winner = player
        elif score[1 - player] >= 24:
            winner = 1 - player

    return winner


def get_possible_moves(board, player):
    minmove = player * 6
    maxmove = (1 + player) * 6
    possible_moves = []

    for i in range(minmove, maxmove):
        if can_play(board, player, i):
            possible_moves.append(i)

    return possible_moves


def get_random_move(board, player):
    possible_moves = get_possible_moves(board, player)
    move = choice(possible_moves)

    return move
