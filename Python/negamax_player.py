from negamax import negamax


class NegamaxPlayer:
    def __init__(self, depth, evaluation):
        """
        :param depth: profondeur d'exploration 
        :param evaluation: fonction d'évaluation utilisée 
        """
        self.depth = depth
        self.evaluation = evaluation

    def get_move(self, awale, player):
        """
        :param awale: état de la partie 
        :param player: numéro du joueur
        :return: indice de la case choisie par le joueur 
        """
        move = negamax(awale, self.depth, player, self.evaluation)[1]

        return move
