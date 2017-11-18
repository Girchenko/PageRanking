class PowerMethod:
    def __init__(self, eps):
        self.iteration = 0
        self.prev = []
        self.eps = eps
        self.is_final_iteration = False

    def convergence(self, previous, current):
        if len(previous) < 1:
            for i in range(len(current)):
                previous.append(0)
        delta = []
        for i in range(len(current)):
            delta.append(abs(current[i]-previous[i]))
        delta_int = 0
        for i in range(len(current)):
            if delta[i] > self.eps:
                delta_int += 1
        self.prev = current.copy()
        if delta_int == 0:
            return True
        return False

    def power_method(self, matrix, rank_vector):
        result = []
        for i in range(len(matrix)):
            result.append(0)
            for j in range(len(matrix)):
                result[i] += abs(matrix[i][j]) * rank_vector[j]
        self.iteration += 1
        return result
