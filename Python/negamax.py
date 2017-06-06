from awale_fun import get_possible_moves


def negamax(awale, depth, player, evaluation):
    """
    Implémente l'algorithme negamax : renvoie le meilleur score et le meilleur coup possibles.
    :param awale: état de la partie
    :param depth: profondeur d'exploration
    :param player: numéro du joueur
    :param evaluation: fonction d'évaluation utilisée 
    :return: meilleur score, meilleur coup
    """
    if awale.winner != -2 or depth == 0:
        return evaluation(awale, player), 6 * player
    else:
        best_score = -float("inf")
        possible_moves = get_possible_moves(awale.board, player)
        best_move = possible_moves[0]

        for i in possible_moves:
            copy_awale = awale.copy()
            copy_awale.play(player, i)
            copy_awale.check_winner(player)
            new_awale = copy_awale.copy()
            score = -negamax(new_awale, depth - 1, 1 - player, evaluation)[0]
            if score > best_score:
                best_score = score
                best_move = i

        return best_score, best_move
