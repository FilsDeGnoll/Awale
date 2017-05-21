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
        moves = []
        for i in range(minmove, maxmove):
            if awale.can_play(player, i):
                moves.append(i)
        move = random.choice(moves)

        return move
