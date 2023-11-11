"""
This script, basic_callbacks.py, forms a crucial part of the basic analytics functionality in the OrestisCompany analytics dashboard. 
It defines and registers callback functions for the Dash app, specifically tailored to update the basic analytics graphs dynamically.

Key Function:
- register_basic_callbacks: 
    Registers callback functions to the Dash app that are triggered by user interactions or automatic intervals. 
    The callbacks update various components of the basic analytics dashboard, ensuring the data displayed is current and interactive.

Callback Details:
- The main callback function, 'update_basic_graphs_live', is designed to update all basic analytics graphs whenever the interval component triggers or the user switches to the basic tab.
- It checks if the current tab is the basic analytics tab; if not, it returns a no_update signal to prevent unnecessary data processing.
- For each graph, it reads the corresponding data from CSV files, processes it using functions from 'basic_views.py', and updates the figures on the dashboard.

The callbacks play a vital role in enhancing the interactivity of the dashboard, allowing for real-time data visualization and ensuring the data presented is refreshed at regular intervals.

Usage:
    To register the callbacks to a Dash app, call the register_basic_callbacks function with the app instance as an argument:
    register_basic_callbacks(app)
"""

from dash.dependencies import Input, Output
from analytics_dashboard.basic.basic_views import create_bar_chart, create_indicator
from analytics_dashboard.basic.data_handling import read_data_basic
from dash import no_update

def register_basic_callbacks(app):
    @app.callback(
        [
            Output('total-sales', 'figure'),
            Output('sales-by-region', 'figure'),
            Output('sales-by-product', 'figure'),
            Output('profit-total', 'figure'),
            Output('profit-by-region', 'figure'),
            Output('profit-by-product', 'figure'),
            Output('top-selling-products', 'figure'),
            Output('top-customers', 'figure'),
            Output('top-stores-by-sales', 'figure'),
        ],
        [Input('basic-interval-component', 'n_intervals')],
        [Input('tabs', 'value')]
    )
    def update_basic_graphs_live(n_intervals, tab):
        if tab != 'tab-basic':  # If it's not the basic tab, return no update
            return [no_update] * 9
        total_sales = create_indicator(read_data_basic('total_sales.csv'), 'Total Sales')
        sales_by_region = create_bar_chart(read_data_basic('sales_by_region.csv', sort_by='sales_by_region', ascending=False), 'Sales by Region')
        sales_by_product = create_bar_chart(read_data_basic('sales_by_product.csv', sort_by='sales_by_product', ascending=False), 'Sales by Product')
        profit_total = create_indicator(read_data_basic('profit_total.csv'), 'Profit Total')
        profit_by_region = create_bar_chart(read_data_basic('profit_by_region.csv', sort_by='profit_by_region', ascending=False), 'Profit by Region')
        profit_by_product = create_bar_chart(read_data_basic('profit_by_product.csv', sort_by='profit_by_product', ascending=False), 'Profit by Product')
        top_selling_products = create_bar_chart(read_data_basic('top_selling_products.csv', sort_by='total_sales', ascending=False), 'Top Selling Products')
        top_customers = create_bar_chart(read_data_basic('top_customers.csv', sort_by='total_spent', ascending=False), 'Top Customers')
        top_stores_by_sales = create_bar_chart(read_data_basic('top_stores_by_sales.csv', sort_by='total_sales', ascending=False), 'Top Stores by Sales')

        return [
            total_sales,
            sales_by_region,
            sales_by_product,
            profit_total,
            profit_by_region,
            profit_by_product,
            top_selling_products,
            top_customers,
            top_stores_by_sales
        ]
