import pandas as pd
import numpy as np 

def taylor_interpolation(dataframe, x_interpolate, n_terms):
    # Extract X and Y values from the dataframe
    x_values = dataframe['X'].tolist()
    y_values = dataframe['Y'].tolist()

    # Initialize an empty dataframe to store the interpolated values
    interpolated_df = pd.DataFrame(columns=['X', 'Y'])
    
    # Iterate through each x value to interpolate
    for x_interp in x_interpolate:
        y_interp = 0.0
        
        # Calculate the coefficients using Taylor series
        for i in range(n_terms):
            term = y_values[i]
            for j in range(i):
                term *= (x_interp - x_values[j]) / (x_values[i] - x_values[j])
            y_interp += term
        
        # Append the interpolated values to the dataframe
        interpolated_df = interpolated_df._append({'X': x_interp, 'Y': y_interp}, ignore_index=True)
    
    return interpolated_df

# Example usage:
# data = pd.DataFrame({'X': [1,2,3], 'Y': [2,2,3]})
# x_interpolate = np.linspace(0,2,100)
# n_terms = 3
# result_df = taylor_interpolation(data, x_interpolate, n_terms)
# print(result_df)

