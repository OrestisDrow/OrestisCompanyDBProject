# basic_views.py
from dash import dcc, html
import plotly.graph_objs as go
from analytics_dashboard.basic.data_handling import read_data_basic

# Function to create a bar chart
def create_bar_chart(data, title):
    if data is not None:
        return {
            'data': [go.Bar(x=data[data.columns[0]], y=data[data.columns[1]], name=title)],
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
                title={"text": title}
            )],
            'layout': {'title': title, 'height': 300}
        }
    else:
        return {
            'data': [],
            'layout': {'title': 'No data found', 'height': 300}
        }

# Function to create the layout for basic analytics
def render_basic_view():
    return html.Div([
            # First row
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='total-sales',
                        figure=create_indicator(read_data_basic('total_sales.csv'), 'Total Sales')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='sales-by-region',
                        figure=create_bar_chart(read_data_basic('sales_by_region.csv', sort_by='sales_by_region', ascending=False), 'Sales by Region')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='sales-by-product',
                        figure=create_bar_chart(read_data_basic('sales_by_product.csv', sort_by='sales_by_product', ascending=False), 'Sales by Product')
                    )
                ], className='grid-item'),
            ], className='row'),
            
            # Second row
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='profit-total',
                        figure=create_indicator(read_data_basic('profit_total.csv'), 'Profit Total')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='profit-by-region',
                        figure=create_bar_chart(read_data_basic('profit_by_region.csv', sort_by='profit_by_region', ascending=False), 'Profit by Region')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='profit-by-product',
                        figure=create_bar_chart(read_data_basic('profit_by_product.csv', sort_by='profit_by_product', ascending=False), 'Profit by Product')
                    )
                ], className='grid-item'),
            ], className='row'),

            # Third row
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='top-selling-products',
                        figure=create_bar_chart(read_data_basic('top_selling_products.csv', sort_by='total_sales', ascending=False), 'Top Selling Products')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='top-customers',
                        figure=create_bar_chart(read_data_basic('top_customers.csv', sort_by='total_spent', ascending=False), 'Top Customers')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='top-stores-by-sales',
                        figure=create_bar_chart(read_data_basic('top_stores_by_sales.csv', sort_by='total_sales', ascending=False), 'Top Stores by Sales')
                    )
                ], className='grid-item'),
            ], className='row'),
        ])
