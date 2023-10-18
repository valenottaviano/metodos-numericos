import pandas as pd

class LagrangeInterpolation:
    def __init__(self, dataframe):
        self.x_values = dataframe['X'].tolist()
        self.y_values = dataframe['Y'].tolist()

    def interpolate(self, x_interpolate):
        interpolated_values = []
        
        for x_interp in x_interpolate:
            y_interp = self._calculate_interpolated_value(x_interp)
            interpolated_values.append((x_interp, y_interp))
        
        interpolated_df = pd.DataFrame(interpolated_values, columns=['X', 'Y'])
        return interpolated_df

    def _calculate_interpolated_value(self, x_interp):
        y_interp = 0.0

        for i in range(len(self.x_values)):
            term = self.y_values[i]

            for j in range(len(self.x_values)):
                if j != i:
                    term *= (x_interp - self.x_values[j]) / (self.x_values[i] - self.x_values[j])
            
            y_interp += term

        return y_interp

    def latex_interpolation_expression(self):
        expression = r"P(x)= "
        raw_expression = r"P(x)= "
        
        for i in range(len(self.x_values)):
            term = round(self.y_values[i], 2)
            term_str = str(term)
            
            for j in range(len(self.x_values)):
                if j != i:
                    term_str += r" \cdot \left(\frac{x - " + str(round(self.x_values[j], 2)) + r"}{" + str(round(self.x_values[i], 2)) + r" - " + str(round(self.x_values[j], 2)) + r"}\right)"
            
            raw_expression += term_str

            if i < 3:
                expression += term_str
            
            if i < len(self.x_values) - 1:
                raw_expression += r" + "
            
            if i < 2:
                expression += r" + "
        
        expression += r"\cdots"
        
        return expression, raw_expression

