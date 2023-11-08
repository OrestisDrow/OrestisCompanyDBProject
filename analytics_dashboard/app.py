from dash import Dash, html, dcc, Input, Output
from analytics_dashboard.layout import get_layout
from analytics_dashboard.basic.basic_callbacks import register_basic_callbacks
from analytics_dashboard.basic.basic_views import render_basic_view

#from intermediate.intermediate_callbacks import register_intermediate_callbacks
#from advanced.advanced_callbacks import register_advanced_callbacks

import sys
sys.path.append('/app')

# Initialize the Dash app
app = Dash(__name__, suppress_callback_exceptions=True)

# Import layouts and register callbacks

app.layout = get_layout()

# Register callbacks
register_basic_callbacks(app)

# The callback function that renders the content based on selected tab
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-basic':
        return render_basic_view()
    elif tab == 'tab-intermediate':
        # Placeholder for intermediate analytics layout function
        return html.Div([
            html.H3('Intermediate analytics coming soon...')
        ])
    elif tab == 'tab-advanced':
        # Placeholder for advanced analytics layout function
        return html.Div([
            html.H3('Advanced analytics coming soon...')
        ])
    
if __name__ == '__main__':
    PORT = 8050
    app.run_server(debug=False, port=PORT, host='0.0.0.0')
