import os
import threading
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Location of the basic analytics CSV files
DATA_DIR = '/app/data/analytics/basic/'

# Function to read CSV data
def read_data(file_name):
    try:
        df = pd.read_csv(os.path.join(DATA_DIR, file_name))
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
    except Exception as e:  # Generic exception catch to handle unforeseen errors
        print(f"An error occurred while reading {file_name}: {e}")
        return None

# Function to create a bar chart
def create_bar_chart(data, title):
    sorted_data = data.sort_values(by=data.columns[1], ascending=False)  # Sort data in descending order based on the second column
    return {
        'data': [go.Bar(x=sorted_data[sorted_data.columns[0]], y=sorted_data[sorted_data.columns[1]], name=title)],
        'layout': {'title': title}
    }

# Function to create a single value indicator
def create_indicator(data, title):
    return {
        'data': [go.Indicator(
            mode="number+delta",
            value=data.iloc[0, 0],
            title={"text": title}
        )],
        'layout': {'title': title}
    }

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(children=[
    html.H1(children='Basic Analytics Dashboard'),
    
    # -----------------------------
    # Total sales indicator
    dcc.Graph(
        id='total-sales',
        figure=create_indicator(read_data('total_sales.csv'), 'Total Sales')
    ),
    
    # Sales by product graph
    dcc.Graph(
        id='sales-by-product',
        figure=create_bar_chart(read_data('sales_by_product.csv'), 'Sales by Product')
    ),

    # Sales by region graph
    dcc.Graph(
        id='sales-by-region',
        figure=create_bar_chart(read_data('sales_by_region.csv'), 'Sales by Region')
    ),

    # -----------------------------
    # Profit total
    dcc.Graph(
        id='profit-total',
        figure=create_indicator(read_data('profit_total.csv'), 'Profit Total')
    ),
    
    # Profit by product
    dcc.Graph(
        id='profit-by-product',
        figure=create_bar_chart(read_data('profit_by_product.csv'), 'Profit by Product')
    ),

    # Profit by region
    dcc.Graph(
        id='profit-by-region',
        figure=create_bar_chart(read_data('profit_by_region.csv'), 'Profit by Region')
    ),
    
    # -----------------------------
    # Top selling products
    dcc.Graph(
        id='top-selling-products',
        figure=create_bar_chart(read_data('top_selling_products.csv'), 'Top Selling Products')
    ),
    
    # Top customers
    dcc.Graph(
        id='top-customers',
        figure=create_bar_chart(read_data('top_customers.csv'), 'Top Customers')
    ),

    # Top Stores by Sales
    dcc.Graph(
        id='top-stores-by-sales',
        figure=create_bar_chart(read_data('top_stores_by_sales.csv'), 'Top Stores by Sales')
    ),
])

def run_dash_server():
    app.run_server(debug=False, use_reloader=False, host='0.0.0.0')

# Run the app
if __name__ == '__main__':
    # Start the server in a new thread
    dash_thread = threading.Thread(target=run_dash_server)#, daemon=True)
    dash_thread.start()
    # Return control back to the CLI
    print("Dash server started! You can now use the CLI for other commands.")