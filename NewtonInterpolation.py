
class NewtonInterpolation:
    def __init__(self):
        self.data = []  # List to store data points (x, y)

    def add_data_point(self, x, y):
        """Add a data point (x, y) to the set."""
        self.data.append((x, y))

    def calculate_coefficients(self):
        """Calculate the coefficients a_i using divided differences."""
        n = len(self.data)
        coefficients = [y for x, y in self.data]

        for j in range(1, n):
            for i in range(n - 1, j - 1, -1):
                coefficients[i] = (coefficients[i] - coefficients[i - 1]) / (self.data[i][0] - self.data[i - j][0])

        return coefficients

    def interpolate(self, x):
        """Interpolate the y value for a given x value."""
        coefficients = self.calculate_coefficients()
        n = len(coefficients)
        result = coefficients[n - 1]

        for i in range(n - 2, -1, -1):
            result = result * (x - self.data[i][0]) + coefficients[i]

        return result



