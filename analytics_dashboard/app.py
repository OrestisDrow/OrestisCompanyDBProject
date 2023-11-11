"""
This script, app.py, serves as the main entry point for the OrestisCompany analytics dashboard, a web-based interface built using Dash. 
The dashboard provides a comprehensive view of the company's analytics across basic, intermediate, and advanced levels. 
It integrates multiple components and callbacks for interactive data visualization and analysis.

Key Features:
1. Modular Layout: 
    Utilizes a modular layout system by importing layout definitions from 'analytics_dashboard.layout'.
2. Tabbed Interface: 
    Offers a tabbed interface to switch between basic, intermediate, and advanced analytics views.
3. Dynamic Content Rendering: 
    Based on the selected tab, appropriate views are rendered dynamically using callback functions.
4. Callback Registration: 
    Registers specific callbacks for each analytics level (basic, intermediate, advanced) to handle user interactions and data updates.
5. Analytics Views: 
    Each analytics level has its own view functions that define the layout and content of that section of the dashboard.

The app is configured to run on port 8050 and listens on all network interfaces. 
It is designed to be user-friendly, providing a centralized platform for accessing different types of analytical insights derived from the company's data.

Usage:
    To start the Dash server and access the analytics dashboard, run:
    python app.py
"""

from dash import Dash, Input, Output
from analytics_dashboard.layout import get_layout

from analytics_dashboard.basic.basic_callbacks import register_basic_callbacks
from analytics_dashboard.basic.basic_views import render_basic_view

from analytics_dashboard.intermediate.intermediate_callbacks import register_intermediate_callbacks
from analytics_dashboard.intermediate.intermediate_views import render_intermediate_view

from analytics_dashboard.advanced.advanced_callbacks import register_advanced_callbacks
from analytics_dashboard.advanced.advanced_views import render_advanced_view

import sys
sys.path.append('/app')

# Initialize the Dash app
app = Dash(__name__, suppress_callback_exceptions=True)

# Import layouts and register callbacks
app.layout = get_layout()

register_basic_callbacks(app)
register_intermediate_callbacks(app)
register_advanced_callbacks(app)

# The callback function that renders the content based on selected tab
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-basic':
        return render_basic_view()
    elif tab == 'tab-intermediate':
        return render_intermediate_view()
    elif tab == 'tab-advanced':
        return render_advanced_view()
    
if __name__ == '__main__':
    PORT = 8050
    app.run_server(debug=False, port=PORT, host='0.0.0.0')
