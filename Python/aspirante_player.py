from aspirante import aspirante


class AspirantePlayer:
    def __init__(self, depth, evaluation):
        self.depth = depth
        self.alpha = -48
        self.beta = 48
        self.evaluation = evaluation

    def get_move_rec(self, awale, player):
        move = aspirante(awale, self.depth, player, self.alpha, self.beta, self.evaluation)

        return move