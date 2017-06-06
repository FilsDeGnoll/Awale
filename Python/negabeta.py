from awale_fun import get_possible_moves


def negabeta(awale, depth, player, alpha, beta, evaluation):
    """
    Implémente l'algorithme negabeta : renvoie le meilleur score et le meilleur coup possibles.
    :param awale: état de la partie
    :param depth: profondeur d'exploration
    :param player: numéro du joueur
    :param alpha: valeur pour l'élagage
    :param beta: valeur pour l'élagage
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
            score = -negabeta(new_awale, depth - 1, 1 - player, -beta, -alpha, evaluation)[0]

            if score > best_score:
                best_score = score
                best_move = i

                if best_score >= alpha:
                    alpha = best_score

                    if alpha >= beta:
                        break

    return best_score, best_move
