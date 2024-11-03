import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State

def create_start_dash_app(requests_pathname_prefix: str = None) -> dash.Dash:
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
            dcc.Interval(id='interval-component', interval=0.2*1000, n_intervals=0),
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

        if len(df) >= 20:
            df = df.iloc[0:0].copy()
        
        random_number = np.random.uniform(-1, 1)
        
        new_point = pd.DataFrame({
            'x': [len(df)],
            'y': [random_number],
            'label': [1 if random_number > 0 else -1]
        })
        df = pd.concat([df, new_point], ignore_index=True)

        figure = generate_figure(df)

        return figure, df.to_dict('records')

    return app

def generate_figure(df):
    fig = go.Figure()

    if len(df) > 0 and df['y'].iloc[0] >= 0:
        fig.add_trace(go.Scatter(
            x=df['x'],
            y=df['y'],
            mode='lines+markers',
            marker=dict(
                size=12,
                line=dict(width=2),
            ),
            line=dict(color='rgba(60,40,0,255)'),
        ))
    else:
        fig.add_trace(go.Bar(
            x=df['x'],
            y=df['y'],
            marker=dict(
                line=dict(width=2, color='rgba(60,40,0,255)')
            )
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
            range=[-1, 20],
            zeroline=False,
        ),
        yaxis=dict(
            title_font=dict(size=14, color='rgba(0,0,0,0)'),
            tickfont=dict(color='rgba(0,0,0,0)'),
            gridcolor='rgba(0,0,0,0)',
            zeroline=True,
            zerolinecolor='rgba(60,40,0,255)',
            zerolinewidth=2,
            range=[-1.1, 1.1]
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    
    return fig
