from math import log2, atan


def evaluation1(awale, player):
    """
    :param awale: état de la partie
    :param player: numéro du joueur
    :return: valeur numérique de l'état du jeu
    """
    return awale.score[player] - awale.score[1 - player]


def eval_1_2(awale, player):
    """
    :param awale: état de la partie
    :param player: numéro du joueur
    :return: valeur numérique de la qualité du territoire du joueur selon le nombre de trous à 1 ou 2 graines
    """
    minmove = 6 * player
    maxmove = 6 * (1 + player)
    s = 0

    for i in range(minmove, maxmove):
        if awale.board[i] == 1 or awale.board[i] == 2:
            s += awale.board[i]

    return s / 12


def eval_krou(awale, player):
    """
    :param awale: état de la partie
    :param player: numéro du joueur
    :return: 1 si le territoire du jeu possède au moins un krou, 0 sinon
    """
    minmove = 6 * player
    maxmove = 6 * (1 + player)
    krou = False
    i = minmove

    while not krou and i < maxmove:
        if 11 - i <= awale.board[i] <= 33 - i:
            krou = True
        i += 1

    return int(krou)


def evaluation2(awale, player):
    """
    :param awale: état de la partie
    :param player: numéro du joueur
    :return: valeur numérique de l'état du jeu
    """
    w = [0.4, 0.1]
    delta_score = awale.score[player] - awale.score[1 - player]
    player_1_2 = eval_1_2(awale, player)  # nombre total de 1-2 chez nous (mauvais)
    opponent_1_2 = eval_1_2(awale, 1 - player)  # nombre total de 1-2 chez l'autre (bon)
    player_krou = eval_krou(awale, player)  # présence d'un krou sur notre terrain (bon)
    opponent_krou = eval_krou(awale, 1 - player)  # présence d'un krou chez l'aversaire (mauvais)
    rep = delta_score + 0.5 + (w[0] * opponent_1_2) + (w[1] * player_krou) - (w[0] * player_1_2) - (
        w[1] * opponent_krou)
    return rep


def attack_coef(awale, player):
    """
    :param awale: état de la partie
    :param player: numéro du joueur
    :return: coefficient d'attaque
    """
    score_player = awale.score[player]
    score_opponent = awale.score[1 - player]
    t1 = log2(score_player + score_opponent + 4) - log2(4)
    t2 = atan(score_player - score_opponent - 7) + atan(score_player - score_opponent + 7)
    n = 2 * (log2(4 + 48) - log2(4))

    return (t1 * t2) / n


def evaluation3(awale, player):
    """
    :param awale: état de la partie
    :param player: numéro du joueur
    :return: valeur numérique de l'état du jeu
    """
    d = 0.4
    score_player = awale.score[player]
    score_opponent = awale.score[1 - player]
    delta_score = score_player - score_opponent
    part_1_2 = 0.8
    part_krou = 1 - part_1_2
    c1 = (part_1_2 / 2) * (1 + attack_coef(score_player, score_opponent))
    c2 = (part_krou / 2) * (1 + attack_coef(score_player, score_opponent))
    c3 = (part_1_2 / 2) * (attack_coef(score_player, score_opponent) - 1)
    c4 = (part_krou / 2) * (attack_coef(score_player, score_opponent) - 1)
    player_1_2 = eval_1_2(awale, player)  # nombre total de 1-2 chez nous (mauvais)
    opponent_1_2 = eval_1_2(awale, 1 - player)  # nombre total de 1-2 chez l'autre (bon)
    player_krou = eval_krou(awale, player)  # présence d'un krou sur notre terrain (bon)
    opponent_krou = eval_krou(awale, 1 - player)  # présence d'un krou chez l'aversaire (mauvais)
    rep = delta_score + (d * (c1 * opponent_1_2) + (c2 * player_krou) + (c3 * player_1_2) + (c4 * opponent_krou))
    return rep
