import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import numpy as np
from taylor import taylor_interpolation

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Define the layout of the app
app.layout = html.Div([
    html.H1("Métodos Numéricos - UNSTA 2023"),

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
        # Scatterplot
        dcc.Graph(id='scatterplot', style={
            'width': '70vw',
            'height': '80vh'
        }),
    ], style={
        'display': 'flex'
    })
], style={
    'min-height': '100vh'
})

# Initialize data
data = {'X': [], 'Y': []}
interpolation_df = pd.DataFrame({'X': [], 'Y': []})

df = pd.DataFrame(data)
interpolation_trace = None  # To store the line trace for interpolation data

@app.callback(
    [Output('scatterplot', 'figure'),
     Output('data-table', 'children')],
    [Input('add-data-btn', 'n_clicks'),
     Input('reset-table-btn', 'n_clicks')],
    [State('x-input', 'value'),
     State('y-input', 'value')]
)
def update_scatterplot_and_table(add_clicks, reset_clicks, x_value, y_value):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    global df
    global interpolation_df
    global interpolation_trace

    if button_id == 'add-data-btn' and add_clicks:
        new_data = {'X': [x_value], 'Y': [y_value]}
        df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)

        n_terms = 3
        if len(df) <= n_terms:
            print('Not enough data')
        else:
            x_interpolate = np.linspace(0, df['X'].max(), 200)
            result_df = taylor_interpolation(df, x_interpolate, n_terms)
            interpolation_df = result_df

    elif button_id == 'reset-table-btn' and reset_clicks:
        df = pd.DataFrame({'X': [], 'Y': []})
        interpolation_df = pd.DataFrame({'X': [], 'Y': []})

    # Create the scatterplot
    fig = px.scatter(df, x='X', y='Y', title='X-Y Scatterplot')

    # Create the data table
    data_table = html.Table([
        html.Tr([html.Th(col) for col in df.columns])] +
        [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(len(df))],
        className='table'
    )

    if not interpolation_df.empty:
        if interpolation_trace is None:
            # Create a new trace for interpolation data
            interpolation_trace = {
                'x': interpolation_df['X'],
                'y': interpolation_df['Y'],
                'mode': 'lines',
                'name': 'Interpolación',
                'line': {'color': 'red'}
            }
            fig.add_trace(interpolation_trace)
            interpolation_trace = None
        else:
            # Update existing trace with new interpolation data
            interpolation_trace['x'] = interpolation_df['X']
            interpolation_trace['y'] = interpolation_df['Y']

    return fig, data_table

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
