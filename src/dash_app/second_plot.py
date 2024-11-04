import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State

def create_second_dash_app(requests_pathname_prefix: str = None) -> dash.Dash:
    initial_data = pd.DataFrame(columns=['x', 'y', 'label'])

    app = dash.Dash(__name__, requests_pathname_prefix=requests_pathname_prefix)

    app.layout = html.Div(
        # style={
        #     'display': 'flex',
        #     'justify-content': 'center',
        #     'align-items': 'center',
        #     'height': '95vh'
        # },
        children=[
            dcc.Graph(
                id='my-graph',
                figure=generate_figure(initial_data),
                # style={'width': '50%', 'height': '50vh'},
                config={'displayModeBar': False},
            ),
            dcc.Interval(id='interval-component', interval=0.15*1000, n_intervals=0),
            dcc.Store(id='data-store', data=initial_data.to_dict('records'))
        ]
    )

    @app.callback(
        Output('my-graph', 'figure'),
        Output('data-store', 'data'),
        Input('interval-component', 'n_intervals'),
        State('data-store', 'data')
    )
    def update_graph(n, stored_data):
        df = pd.DataFrame(stored_data)

        if len(df) >= 100:
            df = df.iloc[0:0].copy()
        
        random_x = np.random.uniform(0.075, 0.6)
        random_y = 1/random_x + np.random.uniform(-2, 2)
        random_number = np.random.uniform(0, 1)
        
        new_point = pd.DataFrame({
            'x': [random_x],
            'y': [random_y],
            'label': [random_number]
        })
        df = pd.concat([df, new_point], ignore_index=True)

        figure = generate_figure(df)

        return figure, df.to_dict('records')

    return app

def generate_figure(df):
    fig = go.Figure()

    if len(df) == 0:
        fig.add_trace(go.Scatter(
        x=df['x'],
        y=df['y'],
        mode='markers',
        marker=dict(
            size=0,  # Multiplica 'label' por un factor para ajustar el tamaño
        ),
    ))
    else:
        fig.add_trace(go.Scatter(
            x=df['x'],
            y=df['y'],
            mode='markers',
            marker=dict(
                size=df['label'] * 12,  # Multiplica 'label' por un factor para ajustar el tamaño
            ),
        ))

    fig.update_traces(
        marker_color=np.where(df['y'] >= 0, 'rgba(160,140,100,255)', 'rgba(160,140,100,255)'),
        marker_line_color='rgba(60,40,0,255)',
        marker_line_width=2,
        hoverinfo='skip',
    )
    fig.update_layout(
        xaxis=dict(
            title_font=dict(size=14, color='rgba(0,0,0,0)'),
            tickfont=dict(color='rgba(0,0,0,0)'),
            gridcolor='rgba(0,0,0,0)',
            range=[0, 0.7],
            zeroline=False,
        ),
        yaxis=dict(
            title_font=dict(size=14, color='rgba(0,0,0,0)'),
            tickfont=dict(color='rgba(0,0,0,0)'),
            gridcolor='rgba(0,0,0,0)',
            zeroline=False,
            zerolinecolor='rgba(60,40,0,255)',
            zerolinewidth=2,
            range=[-0.5, 14.8]
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    
    return fig