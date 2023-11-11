"""
This script, advanced_views.py, is a key component of the advanced analytics section of the OrestisCompany analytics dashboard. 
It defines various visualization components using Dash and Plotly and structures the layout for displaying advanced analytics data.

Functions:
1. create_line_prediction_chart: 
    Generates a line chart with special markers for predicted values, useful for visualizing forecasts.
2. create_multi_line_chart: 
    Creates a line chart with multiple lines, ideal for displaying trends over time with different metrics.
3. create_rfm_score_distribution_chart: 
    Constructs a bar chart to represent the distribution of RFM scores, combined with a line passing through the top middle of each bar.
4. create_scatter_matrix: 
    Generates a scatter plot matrix to visualize relationships between different RFM score components.
5. create_bar_chart: 
    Creates a bar chart, adaptable for various types of data, with an option to handle datasets with more than two columns.
6. render_advanced_view: 
    Organizes the above visualization components into a cohesive layout for the advanced analytics tab in the dashboard.

Each function is designed to handle scenarios where data might not be available or sufficient, displaying a 'No data found' message in such cases. 
The render_advanced_view function ensures that the advanced analytics tab is laid out in a clear, structured, and interactive manner.

Usage:
    The functions in this script are primarily used when rendering the advanced analytics tab on the dashboard. 
    They transform data from CSV files into interactive visualizations, offering deep insights into advanced analytics.
"""

from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
from analytics_dashboard.advanced.data_handling import read_data_advanced
import plotly.express as px

# Function to create a line chart with predicted values
def create_line_prediction_chart(data, title):
    if data is not None:
        last_five = data.iloc[-5:]
        rest = data.iloc[:-5]
        return {
            'data': [
                go.Scatter(x=rest[rest.columns[0]], y=rest[rest.columns[1]], name=title),
                go.Scatter(x=last_five[last_five.columns[0]], y=last_five[last_five.columns[1]], name=title, mode='markers', marker=dict(color='yellow'))
            ],
            'layout': {
                'title': title,
                'height': 500
            }
        }
    else:
        return {
            'data': [],
            'layout': {'title': 'No data found or not enough data points', 'height': 500}
    }

# Function to create a multi line chart
def create_multi_line_chart(data, title):
    if data is not None:
        traces = []
        colors = ['blue', 'green', 'red', 'red']
        for i, col in enumerate(data.columns[1:]):
            if col == 'daily_profit':
                traces.append(go.Scatter(x=data[data.columns[0]], y=data[col], name=col, line=dict(color=colors[1])))
            elif col == 'moving_avg':
                traces.append(go.Scatter(x=data[data.columns[0]], y=data[col], name=col, line=dict(color=colors[0])))
            else:
                traces.append(go.Scatter(x=data[data.columns[0]], y=data[col], name=col, line=dict(color=colors[2])))
        return {
            'data': traces,
            'layout': {
                'title': title,
                'height': 500  
            }
        }
    else:
        return {
            'data': [],
            'layout': {'title': 'No data found or not enough data points', 'height': 500}
        }

# Function to create a bar chart of the distribution of rfm scores, along with a line that passes from the top middle of each bar
def create_rfm_score_distribution_chart(data, title):
    if data is not None:
        # Need to do an extra aggregation step for the chart, 
        # since the same dataset will be used for other plots as well
        rfm_counts = data.groupby('rfm_score')['customer_id'].count().reset_index(name='count')
        fig = go.Figure()
        fig.add_trace(go.Bar(x=rfm_counts['rfm_score'], y=rfm_counts['count'], name=title))
        fig.add_trace(go.Scatter(x=rfm_counts['rfm_score'], y=rfm_counts['count'], mode='lines', name='line', line=dict(color='red')))
        fig.update_layout(
            title={
                'text': title,
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            height=500
        )
        return fig
    else:
        return {
            'data': [],
            'layout': {'title': 'No data found or not enough data points', 'height': 500}
        }

# Function to create a scatter plot matrix
def create_scatter_matrix(data, title):
    if data is not None:
        fig = px.scatter_matrix(data, dimensions=['r_score', 'f_score', 'm_score'], color='rfm_score')
        fig.update_layout(
            title={
                'text': title,
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            height=500
        )
        return fig
    else:
        return {
            'data': [],
            'layout': {'title': 'No data found or not enough data points', 'height': 500}
        }

# Function to create a bar chart
def create_bar_chart(data, title):
    if data is not None:
        if len(data.columns) > 2:
            return {
                'data': [go.Bar(x=data[data.columns[1]], y=data[data.columns[2]], name=title)],
                'layout': {
                    'title': title,
                    'height': 500
                }
            }
        else:
            return {
                'data': [go.Bar(x=data[data.columns[0]], y=data[data.columns[1]], name=title)],
                'layout': {
                    'title': title,
                    'height': 500
                }
            }
    else:
        return {
            'data': [],
            'layout': {'title': 'No data found', 'height': 500}
    }

# Function to create the layout for advaced analytics
def render_advanced_view():
    return html.Div([
            # First row
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='daily-profits-bollinger-bands',
                        figure=create_multi_line_chart(read_data_advanced('daily_profits_bollinger_bands.csv', sort_by='date', ascending=True), 'Bollinger Band, Daily Profits')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='profit-forecasts',
                        figure=create_line_prediction_chart(read_data_advanced('profit_forecast.csv', sort_by='date', ascending=True), 'Profit Forecast')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='product-profit-margins',
                        figure=create_bar_chart(read_data_advanced('product_profit_margins.csv', sort_by='profit_margin', ascending=False), 'Profit Margins per Product')
                    )
                ], className='grid-item'),
            ], className='row'),
            
            # Second row
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='store-profit-margins',
                        figure=create_bar_chart(read_data_advanced('store_profit_margins.csv', sort_by='profit_margin', ascending=False), 'Profit Margins per Store')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='rfm-score-distribution',
                        figure=create_rfm_score_distribution_chart(read_data_advanced('rfm_scores.csv'), 'RFM Score Distribution')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='rfm-score-scatter-plot-matrix',
                        figure=create_scatter_matrix(read_data_advanced('rfm_scores.csv'), 'R-F-M Scatter Plot Matrix')
                    )
                ], className='grid-item'),
            ], className='row'),
        ])