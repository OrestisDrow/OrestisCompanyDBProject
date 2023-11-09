# basic_callbacks.py
from dash.dependencies import Input, Output
from analytics_dashboard.intermediate.intermediate_views import create_line_chart, create_indicator
from analytics_dashboard.intermediate.data_handling import read_data_intermediate
from dash import no_update

def register_intermediate_callbacks(app):
    @app.callback(
        [
            Output('avg-purchase-per-customer', 'figure'),
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
        avg_purchase_per_customer = create_line_chart(read_data_intermediate('avg_purchase_per_customer.csv', sort_by='avg_purchase_value', ascending=False),'Avg Purchase per Customer')
        avg_sales_by_weekday = create_line_chart(read_data_intermediate('avg_sales_by_weekday.csv', sort_by='weekday', ascending=True), 'Avg Sales by Weekday')
        avg_purchase_frequency = create_indicator(read_data_intermediate('avg_purchase_frequency.csv'), 'Avg Purchase Frequency')
        monthly_sales_trend = create_line_chart(read_data_intermediate('monthly_sales_trend.csv', sort_by='YearMonth', ascending=True), 'Monthly Sales Trend')
        sales_by_day_of_month = create_line_chart(read_data_intermediate('sales_by_day_of_month.csv', sort_by='day', ascending=True), 'Sales by Day of Month')
        
        return [
            avg_purchase_per_customer,
            avg_sales_by_weekday,
            avg_purchase_frequency,
            monthly_sales_trend,
            sales_by_day_of_month,
        ]
