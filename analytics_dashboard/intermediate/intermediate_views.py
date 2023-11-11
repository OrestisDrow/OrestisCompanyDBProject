"""
This script, intermediate_views.py, is part of the intermediate analytics section of the OrestisCompany analytics dashboard. 
It defines visualization components and structures the layout for displaying intermediate analytics data. 
The script utilizes Dash and Plotly for creating interactive graphs and charts.

Functions:
1. create_line_chart: 
    Generates a line chart given a DataFrame. It expects the data to have the first column for the x-axis and the second for the y-axis.
2. create_indicator: 
    Constructs a numerical indicator visualization, used for displaying single-value metrics like average purchase value or frequency.
3. render_intermediate_view: 
    Arranges the visualization components into a layout for the intermediate analytics tab in the dashboard.

The functions handle the absence of data gracefully, displaying 'No data found' in such scenarios. 
The render_intermediate_view function organizes the graphs into a grid layout, providing a clear and structured presentation of the intermediate analytics.

Usage:
    The functions in this script are mainly invoked when rendering the intermediate analytics tab in the dashboard. 
    They access prepared data from CSV files, process it, and present it in a web-based interface for interactive analysis.
"""

from dash import dcc, html
import plotly.graph_objs as go
from analytics_dashboard.intermediate.data_handling import read_data_intermediate

# Function to create a line chart
def create_line_chart(data, title):
    if data is not None:
        return {
            'data': [go.Scatter(x=data[data.columns[0]], y=data[data.columns[1]], name=title)],
            'layout': {
                'title': title,
                'height': 300
            }
        }
    else:
        return {
            'data': [],
            'layout': {'title': 'No data found', 'height': 300}
    }

# Function to create a single value indicator
def create_indicator(data, title):
    if data is not None and not data.empty:
        return {
            'data': [go.Indicator(
                mode="number+delta",
                value=data.iloc[0, 0],
            )],
            'layout': {'title': title, 'height': 300}
        }
    else:
        return {
            'data': [],
            'layout': {'title': 'No data found', 'height': 300}
        }

# Function to create the layout for intermediate analytics
def render_intermediate_view():
    return html.Div([
            # First row
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='avg-purchase',
                        figure=create_indicator(read_data_intermediate('avg_purchase.csv'), 'Avg Purchase Value')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='avg-sales-by-weekday',
                        figure=create_line_chart(read_data_intermediate('avg_sales_by_weekday.csv', sort_by='weekday', ascending=True), 'Avg Sales by Weekday')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='customer-frequency',
                        figure=create_indicator(read_data_intermediate('avg_purchase_frequency.csv'), 'Avg Purchase Frequency')
                    )
                ], className='grid-item'),
            ], className='row'),
            
            # Second row
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='monthly-sales-trend',
                        figure=create_line_chart(read_data_intermediate('monthly_sales_trend.csv', sort_by='YearMonth', ascending=True), 'Monthly Sales Trend')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='sales-by-day-of-month',
                        figure=create_line_chart(read_data_intermediate('sales_by_day_of_month.csv', sort_by='day', ascending=True), 'Sales by Day of Month')
                    )
                ], className='grid-item'),
            ], className='row'),
        ])