from aspirante import aspirante


class AspirantePlayer:
    def __init__(self, depth, evaluation,alpha,beta):
        self.depth = depth
        self.alpha = alpha
        self.beta = beta
        self.evaluation = evaluation

    def get_move_rec(self, awale, player):
        move = aspirante(awale, self.depth, player, self.alpha, self.beta, self.evaluation)

        return move