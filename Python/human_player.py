class HumanPlayer:
    @staticmethod
    def get_move(awale, player):
        """
        :param awale: état de la partie
        :param player: numéro du joueur
        :return: indice de la case choisie par le joueur
        """
        try:
            move = int(input("Choisissez une case : "))
        except ValueError:
            move = -1

        while not awale.can_play(player, move):
            try:
                move = int(input("Le coup est invalide, choisissez une autre case : "))
            except ValueError:
                move = -1

        return move
