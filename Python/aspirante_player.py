from aspirante import aspirante


class AspirantePlayer:
    def __init__(self, depth, evaluation):
        """
        :param depth: profondeur d'exploration 
        :param evaluation: fonction d'évaluation utilisée
        """
        self.depth = depth
        self.alpha = -24
        self.beta = 24
        self.evaluation = evaluation

    def get_move(self, awale, player):
        """
        :param awale: état de la partie 
        :param player: numéro du joueur
        :return: indice de la case choisie par le joueur 
        """
        move = aspirante(awale, self.depth, player, self.alpha, self.beta, self.evaluation)[1]

        return move
