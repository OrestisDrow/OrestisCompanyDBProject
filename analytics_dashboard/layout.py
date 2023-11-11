"""
This script, layout.py, is part of the OrestisCompany analytics dashboard. 
It defines the overall layout of the web-based dashboard built using Dash. 
The layout configuration ensures a cohesive and intuitive user interface for navigating various analytics insights.

Key Features of the Dashboard Layout:
1. Main Title: 
    Displays the title 'Orestis Company Analytics Dashboard' centered at the top of the page.
2. Interval Components: 
    Includes three dcc.Interval components for basic, intermediate, and advanced analytics. These are set to trigger at 10-second intervals, facilitating periodic updates.
3. Tabbed Navigation: 
    Provides a tabbed interface for easy navigation between different analytics views - Basic, Intermediate, and Advanced.
4. Content Container: 
    A dynamic content area (`tabs-content`) which updates to display content relevant to the selected tab.

The `get_layout` function returns a Dash HTML Div element containing the entire layout structure. 
This modular approach allows for easy maintenance and updates to the dashboard's appearance and functionality.

Usage:
    To apply this layout to a Dash app, import the `get_layout` function and set the app layout:
    app.layout = get_layout()
"""

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
        dcc.Interval(
            id='advanced-interval-component',
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
