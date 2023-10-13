
class NewtonInterpolation:
    def __init__(self):
        self.data = []  # Lista para almacenar los puntos de datos (x, y)

    def add_data_point(self, x, y):
        """Agrega un punto de datos (x, y) al conjunto."""
        self.data.append((x, y))

    def calculate_coefficients(self):
        """Calcula los coeficientes a_i usando diferencias divididas."""
        n = len(self.data)
        coefficients = [y for x, y in self.data]

        for j in range(1, n):
            for i in range(n - 1, j - 1, -1):
                coefficients[i] = (coefficients[i] - coefficients[i - 1]) / (self.data[i][0] - self.data[i - j][0])

        return coefficients

    def interpolate(self, x):
        """Interpola el valor de y para un valor de x dado."""
        coefficients = self.calculate_coefficients()
        n = len(coefficients)
        result = coefficients[n - 1]

        for i in range(n - 2, -1, -1):
            result = result * (x - self.data[i][0]) + coefficients[i]

        return result


