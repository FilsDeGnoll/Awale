from aspirante import aspirante


class AspirantePlayer:
    def __init__(self, depth, evaluation):
        self.depth = depth
        self.alpha = -24
        self.beta = 24
        self.evaluation = evaluation

    def get_move(self, awale, player):
        move = aspirante(awale, self.depth, player, self.alpha, self.beta, self.evaluation)[1]

        return move