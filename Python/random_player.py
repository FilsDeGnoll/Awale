from awale_fun import get_random_move


class RandomPlayer:
    @staticmethod
    def get_move(awale, player):
        """
        :param awale: état de la partie
        :param player: numéro du joueur
        :return: indice de la case choisie par le joueur
        """
        move = get_random_move(awale.board, player)

        return move
