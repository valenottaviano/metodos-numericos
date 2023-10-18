import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import numpy as np
from LagrangeInterpolation import LagrangeInterpolation
from NewtonInterpolation import NewtonInterpolation



# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Define the layout of the app
app.layout = html.Div([
    html.H1("Métodos Numéricos - UNSTA 2023"),
    html.H3("Interpolación de Lagrange"),
    dcc.Markdown("", mathjax=True, id='latex_expresssion_lagrange'),
    html.H3("Interpolación de Newton"),
    dcc.Markdown("", mathjax=True, id='latex_expresssion_newton'),
    html.Div([
        # Input table
        html.Div([
            dcc.Input(id='x-input', type='number', placeholder='Enter X'),
            dcc.Input(id='y-input', type='number', placeholder='Enter Y'),
            html.Div([
                html.Button(
                    'Add Data',
                    id='add-data-btn',
                    className='button-primary',
                    style={
                        'margin-right': '1rem'
                    }),
                html.Button('Reset Table', id='reset-table-btn'),
            ], style={
                'display': 'flex',
                'justify-content': 'center',
                'margin-top': '2rem',
            }),
            # Data table
            html.Div(id='data-table')
        ],
        style={
            'display': 'flex',
            'flex-direction': 'column',
            'align-items': 'center',
            'width': '30vw',
            'margin': 'auto',
            'padding': '3rem'
        }),
        # Scatterplot for Lagrange Interpolation
        html.Div([
            dcc.Graph(id='scatterplot-lagrange', style={
                        'width': '60vw',
                        'height': '50vh'
                    }),
        # Scatterplot for Newton Interpolation
        dcc.Graph(id='scatterplot-newton', style={
            'width': '60vw',
            'height': '50vh'
        }),
        ])
    ], style={
        'display': 'flex',
    }),
    html.H3("Interpolación de Lagrange"),
    dcc.Markdown("", mathjax=False, id='latex_expresssion_lagrange_raw'),
    html.H3("Interpolación de Newton"),
    dcc.Markdown("", mathjax=False, id='latex_expresssion_newton_raw'),
], style={
    'min-height': '100vh',
    'width': '80vw',
    'margin' : 'auto',
    'display': 'flex',
    'flex-direction': 'column',
    'align-items': 'center',
})


np.random.seed(0)  # For reproducibility
num_elements = 5

x_values = np.sort(np.random.uniform(0, 10, num_elements))
y_values = np.sin(x_values) 

dummy_data = pd.DataFrame({'X': x_values, 'Y': y_values})

data = dummy_data
interpolation_df_lagrange = pd.DataFrame({'X': [], 'Y': []})
interpolation_df_newton = pd.DataFrame({'X': [], 'Y': []})

df = pd.DataFrame(data)
interpolation_trace_lagrange = None  # To store the line trace for interpolation data
interpolation_trace_newton = None  # To store the line trace for interpolation data

latex_expression_lagrange = r'$\text{No interpolation}$'
latex_expression_newton = r'$\text{No interpolation}$'
raw_lagrange = ''
raw_newton = ''

@app.callback(
    [Output('scatterplot-lagrange', 'figure'),
     Output('scatterplot-newton', 'figure'),
     Output('data-table', 'children'),
     Output('latex_expresssion_lagrange', 'children'),
     Output('latex_expresssion_newton', 'children'),
     Output('latex_expresssion_lagrange_raw', 'children'),
     Output('latex_expresssion_newton_raw', 'children')
     ],
    [Input('add-data-btn', 'n_clicks'),
     Input('reset-table-btn', 'n_clicks')],
    [State('x-input', 'value'),
     State('y-input', 'value')]
)
def update_scatterplots_and_table(add_clicks, reset_clicks, x_value, y_value):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    global df
    global interpolation_df_lagrange
    global interpolation_df_newton
    global interpolation_trace_lagrange
    global interpolation_trace_newton
    global latex_expression_lagrange
    global latex_expression_newton
    global raw_lagrange
    global raw_newton

    if button_id == 'add-data-btn' and add_clicks:
        new_data = {'X': [x_value], 'Y': [y_value]}
        df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)

        if len(df) == 1:
            print('Not enough data')
        else:
            lagrange_interpolator = LagrangeInterpolation(df)
            newton_interpolator = NewtonInterpolation(df)

            x_interpolate = np.linspace(0, df['X'].max(), 200)
            
            result_df_lagrange = lagrange_interpolator.interpolate(x_interpolate)
            result_df_newton = newton_interpolator.interpolate(x_interpolate)

            latex_expression_lagrange, raw_lagrange = lagrange_interpolator.latex_interpolation_expression()
            latex_expression_newton, raw_newton = newton_interpolator.latex_interpolation_expression()

            latex_expression_lagrange = "$" + latex_expression_lagrange.strip() + "$"
            latex_expression_newton = "$" + latex_expression_newton.strip() + "$"

            interpolation_df_lagrange = result_df_lagrange
            interpolation_df_newton = result_df_newton

    elif button_id == 'reset-table-btn' and reset_clicks:
        df = pd.DataFrame({'X': [], 'Y': []})
        interpolation_df_lagrange = pd.DataFrame({'X': [], 'Y': []})
        latex_expression_lagrange = r'$\text{No interpolation}$'
        raw_lagrange = r'No interpolation'

        interpolation_df_newton = pd.DataFrame({'X': [], 'Y': []})
        latex_expression_newton = r'$\text{No interpolation}$'
        raw_newton = r'No interpolation'

    # Create the data table
    data_table = html.Table([
        html.Tr([html.Th(col) for col in df.columns])] +
        [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(len(df))],
        className='table'
    )

    # Create the scatterplots for Lagrange and Newton interpolations
    fig_lagrange = px.scatter(df, x='X', y='Y')
    fig_newton = px.scatter(df, x='X', y='Y')

    if not interpolation_df_lagrange.empty:
        if interpolation_trace_lagrange is None:
            # Create a new trace for Lagrange interpolation data
            interpolation_trace_lagrange = {
                'x': interpolation_df_lagrange['X'],
                'y': interpolation_df_lagrange['Y'],
                'mode': 'lines',
                'name': 'Lagrange',
                'line': {'color': 'red'}
            }
            fig_lagrange.add_trace(interpolation_trace_lagrange)
            interpolation_trace_lagrange = None
        else:
        # Update existing trace with new Lagrange interpolation data
            interpolation_trace_lagrange['x'] = interpolation_df_lagrange['X']
            interpolation_trace_lagrange['y'] = interpolation_df_lagrange['Y']

    if not interpolation_df_newton.empty:
        if interpolation_trace_newton is None:
            # Create a new trace for Newton interpolation data
            interpolation_trace_newton = {
                'x': interpolation_df_newton['X'],
                'y': interpolation_df_newton['Y'],
                'mode': 'lines',
                'name': 'Newton',
                'line': {'color': 'blue'}
            }
            fig_newton.add_trace(interpolation_trace_newton)
            interpolation_trace_newton = None
        else:
            interpolation_trace_newton['x'] = interpolation_df_newton['X']
            interpolation_trace_newton['y'] = interpolation_df_newton['Y']

    return fig_lagrange, fig_newton, data_table, latex_expression_lagrange, latex_expression_newton, raw_lagrange, raw_newton

# Run the app
if __name__ == '__main__':
    
    app.run_server(debug=True)
