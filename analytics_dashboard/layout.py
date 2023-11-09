from dash import html, dcc

def get_layout():
    return html.Div([
        html.H1('Orestis Company Analytics Dashboard', style={'textAlign': 'center'}),
        dcc.Interval(
            id='basic-interval-component',
            interval=10*1000,  
            n_intervals=0
        ),
        dcc.Interval(
            id='intermediate-interval-component',
            interval=10*1000,  
            n_intervals=0
        ),
        dcc.Tabs(id='tabs', value='tab-basic', children=[
            dcc.Tab(label='Basic', value='tab-basic'),
            dcc.Tab(label='Intermediate', value='tab-intermediate'),
            dcc.Tab(label='Advanced', value='tab-advanced'),
        ], style={'marginBottom': '10px'}),
        html.Div(id='tabs-content')
    ])
