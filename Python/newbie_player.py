from awale_fun import get_possible_moves

class NewbiePlayer:
    @staticmethod
    def best_move(awale, player):
        """
        :param awale: état de la partie 
        :param player: numéro du joueur
        :return: meilleur coup
        """
        possible_moves = get_possible_moves(awale.board, player)
        best_move = possible_moves[0]
        best_score = awale.pick(player, best_move)[1][player]

        for i in possible_moves[1:]:
            new_score = awale.pick(player, i)[1][player]
            if new_score > best_score:
                best_move = i

        return best_move

    @staticmethod
    def get_move(awale, player):
        """
        :param awale: état de la partie 
        :param player: numéro du joueur
        :return: indice de la case choisie par le joueur 
        """
        move = NewbiePlayer.best_move(awale, player)

        return move
