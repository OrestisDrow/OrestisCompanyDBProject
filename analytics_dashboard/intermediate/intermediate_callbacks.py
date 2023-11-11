"""
This script, intermediate_callbacks.py, is an essential component of the intermediate analytics module in the OrestisCompany analytics dashboard. 
It defines and registers callback functions for the Dash app, specifically for updating the intermediate analytics graphs based on user interactions or automatic intervals.

Function:
- register_intermediate_callbacks: 
    This function registers callback functions to the Dash app. These callbacks are responsible for dynamically updating various components of the intermediate analytics dashboard, ensuring the data displayed is fresh and responsive to user actions.

Callback Details:
- The primary callback function, 'update_intermediate_graphs_live', is designed to refresh all intermediate analytics graphs whenever the interval component triggers or when the user navigates to the intermediate tab.
- It checks if the current tab is the intermediate analytics tab; if not, it returns a no_update signal to prevent unnecessary data processing.
- Each graph's content is updated by reading the corresponding data from CSV files, processing it using functions from 'intermediate_views.py', and updating the figures on the dashboard.

These callbacks enhance the interactivity of the dashboard, providing users with a dynamic and engaging experience by enabling real-time data visualization and ensuring regular data updates.

Usage:
    To integrate these callbacks into a Dash app, the register_intermediate_callbacks function is called with the app instance as an argument:
    register_intermediate_callbacks(app)
"""

from dash.dependencies import Input, Output
from analytics_dashboard.intermediate.intermediate_views import create_line_chart, create_indicator
from analytics_dashboard.intermediate.data_handling import read_data_intermediate
from dash import no_update

def register_intermediate_callbacks(app):
    @app.callback(
        [
            Output('avg-purchase', 'figure'),
            Output('avg-sales-by-weekday', 'figure'),
            Output('avg-purchase-frequency', 'figure'),
            Output('monthly-sales-trend', 'figure'),
            Output('sales-by-day-of-month', 'figure'),
        ],
        [Input('intermediate-interval-component', 'n_intervals')],
        [Input('tabs', 'value')]
    )
    def update_intermediate_graphs_live(n_intervals, tab):
        if tab != 'tab-intermediate':
            return [no_update] * 5
        print("Updating intermediate graphs")
        avg_purchase = create_indicator(read_data_intermediate('avg_purchase.csv'),'Avg Purchase Value')
        avg_sales_by_weekday = create_line_chart(read_data_intermediate('avg_sales_by_weekday.csv', sort_by='weekday', ascending=True), 'Avg Sales by Weekday')
        avg_purchase_frequency = create_indicator(read_data_intermediate('avg_purchase_frequency.csv'), 'Avg Purchase Frequency')
        monthly_sales_trend = create_line_chart(read_data_intermediate('monthly_sales_trend.csv', sort_by='YearMonth', ascending=True), 'Monthly Sales Trend')
        sales_by_day_of_month = create_line_chart(read_data_intermediate('sales_by_day_of_month.csv', sort_by='day', ascending=True), 'Sales by Day of Month')
        
        return [
            avg_purchase,
            avg_sales_by_weekday,
            avg_purchase_frequency,
            monthly_sales_trend,
            sales_by_day_of_month,
        ]
