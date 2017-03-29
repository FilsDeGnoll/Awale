import random


class RandomPlayer:
    @staticmethod
    def get_move(awale, player):
        """
        :param awale: état de la partie
        :param player: numéro du joueur
        :return: indice de la case choisie par le joueur
        """
        minmove = player * 6
        maxmove = (1 + player) * 6
        move = -1

        # TODO: choisir parmi les coups possibles ?
        while not awale.can_play(player, move):
            move = random.randint(minmove, maxmove)

        return move
