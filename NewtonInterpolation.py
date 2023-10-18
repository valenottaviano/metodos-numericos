import pandas as pd

class NewtonInterpolation:
    def __init__(self, dataframe):
        self.x_values = dataframe['X'].tolist()
        self.y_values = dataframe['Y'].tolist()
        self.divided_differences = self.calculate_divided_differences()

    def calculate_divided_differences(self):
        n = len(self.x_values)
        divided_differences = [[0] * n for _ in range(n)]

        for i in range(n):
            divided_differences[i][0] = self.y_values[i]

        for j in range(1, n):
            for i in range(n - j):
                divided_differences[i][j] = (divided_differences[i + 1][j - 1] - divided_differences[i][j - 1]) / (self.x_values[i + j] - self.x_values[i])

        return divided_differences

    def interpolate(self, x_interpolate):
        interpolated_values = []
        
        for x_interp in x_interpolate:
            y_interp = self._calculate_interpolated_value(x_interp)
            interpolated_values.append((x_interp, y_interp))
        
        interpolated_df = pd.DataFrame(interpolated_values, columns=['X', 'Y'])
        return interpolated_df

    def _calculate_interpolated_value(self, x_interp):
        n = len(self.x_values)
        y_interp = self.divided_differences[0][0]
        temp = 1.0

        for i in range(1, n):
            temp *= (x_interp - self.x_values[i - 1])
            y_interp += temp * self.divided_differences[0][i]

        return y_interp

    def latex_interpolation_expression(self):
        expression = r"P(x)= "
        raw_expression = r"P(x)= "
        
        for i in range(len(self.x_values)):
            term = self.divided_differences[0][i]
            term_str = str(round(term,2))
            
            for j in range(i):
                term_str += r" \cdot (x - " + str(round(self.x_values[j], 2)) + r")"
            
            raw_expression += term_str
            
            if i < 4:
                expression += term_str
            
            if i < len(self.x_values) - 1:
                raw_expression += r" + "
            
            if i < 3:
                expression += r" + "
        
        if len(self.x_values) > 4:
            expression += r"\cdots"
        
        
        return expression, raw_expression
