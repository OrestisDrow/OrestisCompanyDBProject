import os
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import socket
from contextlib import closing

# Location of the analytics CSV files
DATA_DIR = '/app/data/analytics/'

# Function to read CSV data
def read_data(file_name, sort_by=None, ascending=False):
    try:
        df = pd.read_csv(os.path.join(DATA_DIR, file_name))
        if sort_by and sort_by in df.columns:
            df = df.sort_values(by=sort_by, ascending=ascending)
        return df
    except FileNotFoundError:
        print(f"The file {file_name} was not found in the directory.")
        return None
    except pd.errors.EmptyDataError:
        print(f"The file {file_name} is empty.")
        return None
    except pd.errors.ParserError:
        print(f"The file {file_name} contains parsing errors.")
        return None
    except Exception as e:  # Handle unforeseen errors
        print(f"An error occurred while reading {file_name}: {e}")
        return None

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
    
# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout with tabs
app.layout = html.Div([
    html.H1('Orestis Company Analytics Dashboard', style={'textAlign': 'center'}),
    # 10 seconds update intervals if even a single .csv changes
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  
        n_intervals=0
    ),
    # Tabs
    dcc.Tabs(id='tabs', value='tab-basic', children=[
        dcc.Tab(label='Basic', value='tab-basic'),
        dcc.Tab(label='Intermediate', value='tab-intermediate'),
        dcc.Tab(label='Advanced', value='tab-advanced'),
    ], style={'marginBottom': '10px'}),
    
    # Content for tabs will be rendered by the callback below
    html.Div(id='tabs-content')
])

# The callback function that renders the content
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-basic':
        # Return the layout for basic analytics
        return html.Div([
            # First row
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='total-sales',
                        figure=create_indicator(read_data('basic/total_sales.csv'), 'Total Sales')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='sales-by-region',
                        figure=create_bar_chart(read_data('basic/sales_by_region.csv', sort_by='sales_by_region', ascending=False), 'Sales by Region')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='sales-by-product',
                        figure=create_bar_chart(read_data('basic/sales_by_product.csv', sort_by='sales_by_product', ascending=False), 'Sales by Product')
                    )
                ], className='grid-item'),
            ], className='row'),
            
            # Second row
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='profit-total',
                        figure=create_indicator(read_data('basic/profit_total.csv'), 'Profit Total')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='profit-by-region',
                        figure=create_bar_chart(read_data('basic/profit_by_region.csv', sort_by='profit_by_region', ascending=False), 'Profit by Region')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='profit-by-product',
                        figure=create_bar_chart(read_data('basic/profit_by_product.csv', sort_by='profit_by_product', ascending=False), 'Profit by Product')
                    )
                ], className='grid-item'),
            ], className='row'),

            # Third row
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='top-selling-products',
                        figure=create_bar_chart(read_data('basic/top_selling_products.csv', sort_by='total_sales', ascending=False), 'Top Selling Products')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='top-customers',
                        figure=create_bar_chart(read_data('basic/top_customers.csv', sort_by='total_spent', ascending=False), 'Top Customers')
                    )
                ], className='grid-item'),
                html.Div([
                    dcc.Graph(
                        id='top-stores-by-sales',
                        figure=create_bar_chart(read_data('basic/top_stores_by_sales.csv', sort_by='total_sales', ascending=False), 'Top Stores by Sales')
                    )
                ], className='grid-item'),
            ], className='row'),
        ])
    
    elif tab == 'tab-intermediate':
        # Since intermediate analytics isn't implemented yet, show placeholder
        return html.Div([
            html.H3('Intermediate analytics coming soon...')
        ])
    elif tab == 'tab-advanced':
        # Since advanced analytics isn't implemented yet, show placeholder
        return html.Div([
            html.H3('Advanced analytics coming soon...')
        ])
    
# Function to update figures with sorting
def update_figure(data_func, file_name, chart_func, chart_title, sort_by=None, ascending=False):
    df = data_func(file_name, sort_by=sort_by, ascending=ascending)
    return chart_func(df, chart_title)


# The callback to update the graphs, you will need one for each graph
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
    [Input('interval-component', 'n_intervals')]
)
def update_graph_live(n_intervals):
    total_sales = update_figure(read_data, 'basic/total_sales.csv', create_indicator, 'Total Sales')
    sales_by_region = update_figure(read_data, 'basic/sales_by_region.csv', create_bar_chart, 'Sales by Region', sort_by='sales_by_region', ascending=False)
    sales_by_product = update_figure(read_data, 'basic/sales_by_product.csv', create_bar_chart, 'Sales by Product', sort_by='sales_by_product', ascending=False)
    profit_total = update_figure(read_data, 'basic/profit_total.csv', create_indicator, 'Profit Total')
    profit_by_region = update_figure(read_data, 'basic/profit_by_region.csv', create_bar_chart, 'Profit by Region', sort_by='profit_by_region', ascending=False)
    profit_by_product = update_figure(read_data, 'basic/profit_by_product.csv', create_bar_chart, 'Profit by Product', sort_by='profit_by_product', ascending=False)
    top_selling_products = update_figure(read_data, 'basic/top_selling_products.csv', create_bar_chart, 'Top Selling Products', sort_by='total_sales', ascending=False)
    top_customers = update_figure(read_data, 'basic/top_customers.csv', create_bar_chart, 'Top Customers', sort_by='total_spent', ascending=False)
    top_stores_by_sales = update_figure(read_data, 'basic/top_stores_by_sales.csv', create_bar_chart, 'Top Stores by Sales', sort_by='total_sales', ascending=False)

    # Return all the updated figures
    return [total_sales, sales_by_region, sales_by_product, profit_total, profit_by_region, profit_by_product, top_selling_products, top_customers, top_stores_by_sales]

def check_port(port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex(('localhost', port)) == 0:
            return True # The port is open
        else:
            return False # The port is closed

# Run the app
if __name__ == '__main__':
    """
    The Dash server for visualizations will run on port 8050, if the port is busy/closed
    this would mean that the server is already running.
    """
    PORT = 8050
    if not check_port(PORT):
        # Start the Dash app
        app.run_server(debug=False, port=PORT, host='0.0.0.0')
