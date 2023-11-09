# basic_views.py
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
                'height': 300  # Set the height of the graph
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
                        id='avg-purchase-per-customer',
                        figure=create_line_chart(read_data_intermediate('avg_purchase_per_customer.csv', sort_by='avg_purchase_value', ascending=False), 'Avg Purchase per Customer')
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