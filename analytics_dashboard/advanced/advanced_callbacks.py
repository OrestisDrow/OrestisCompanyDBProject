"""
This script, advanced_callbacks.py, is integral to the advanced analytics functionality of the OrestisCompany analytics dashboard. 
It establishes and registers callback functions for the Dash app, specifically focused on updating the advanced analytics graphs in response to user interactions or set intervals.

Function:
- register_advanced_callbacks: Registers callback functions to the Dash app that update components of the advanced analytics dashboard. These callbacks ensure that the displayed data is current and interactive.

Callback Details:
- The 'update_advanced_graphs_live' function is the core callback that refreshes all the advanced analytics graphs. It is triggered by the interval component or when the user navigates to the advanced tab.
- The function checks if the current tab is the advanced analytics tab; if not, it returns a no_update signal to avoid unnecessary data processing.
- Each graph is updated by reading relevant data from CSV files, using visualization functions from 'advanced_views.py', and refreshing the figures on the dashboard.

These callbacks enhance the dashboard's interactivity, providing a dynamic user experience with real-time data visualization and ensuring that the displayed data is refreshed at regular intervals.

Usage:
    To integrate these callbacks into a Dash app, the register_advanced_callbacks function is called with the app instance as an argument:
    register_advanced_callbacks(app)
"""

from dash.dependencies import Input, Output
from analytics_dashboard.advanced.advanced_views import *
from analytics_dashboard.advanced.data_handling import read_data_advanced
from dash import no_update

def register_advanced_callbacks(app):
    @app.callback(
        [
            Output('daily-profits-bollinger-bands', 'figure'),
            Output('profit-forecasts', 'figure'),
            Output('product-profit-margins', 'figure'),
            Output('store-profit-margins', 'figure'),
            Output('rfm-score-distribution', 'figure'),
            Output('rfm-score-scatter-plot-matrix', 'figure'),
        ],
        [Input('advanced-interval-component', 'n_intervals')],
        [Input('tabs', 'value')]
    )
    def update_advanced_graphs_live(n_intervals, tab):
        if tab != 'tab-advanced':
            return [no_update] * 6
        daily_profits_bollinger_bands = create_multi_line_chart(read_data_advanced('daily_profits_bollinger_bands.csv', sort_by='date', ascending=True), 'Bollinger Band on Daily Profits')
        profit_forecasts = create_line_prediction_chart(read_data_advanced('profit_forecast.csv', sort_by='date', ascending=True), 'Profit Forecast')
        product_profit_margins = create_bar_chart(read_data_advanced('product_profit_margins.csv', sort_by='profit_margin', ascending=False), 'Profit Margins per Product')
        store_profit_margins = create_bar_chart(read_data_advanced('store_profit_margins.csv', sort_by='profit_margin', ascending=False), 'Profit Margins per Store')
        rfm_score_distribution = create_rfm_score_distribution_chart(read_data_advanced('rfm_scores.csv'), 'RFM Score Distribution')
        rfm_score_scatter_plot_matrix = create_scatter_matrix(read_data_advanced('rfm_scores.csv'), 'R-F-M Scatter Plot Matrix')
        return [
            daily_profits_bollinger_bands,
            profit_forecasts,
            product_profit_margins,
            store_profit_margins,
            rfm_score_distribution,
            rfm_score_scatter_plot_matrix
        ]
