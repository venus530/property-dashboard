import dash
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
import os

# Load data
csv_file = 'PROPERTYVALUATIONS.csv'
df = pd.read_csv(csv_file)

# Summary statistics
num_properties = len(df)
avg_market_value = df['Market Value'].mean()
median_market_value = df['Market Value'].median()
avg_land_rate = df['Land Rate'].mean()

# App
app = dash.Dash(__name__)
server = app.server  # Need this for deployment

app.layout = html.Div([
    html.H1('Property Valuation Dashboard'),
    html.Div([
        html.Div([
            html.H3('Total Properties'),
            html.P(f"{num_properties}")
        ], style={'width': '24%', 'display': 'inline-block'}),
        html.Div([
            html.H3('Avg. Market Value'),
            html.P(f"{avg_market_value:,.2f}")
        ], style={'width': '24%', 'display': 'inline-block'}),
        html.Div([
            html.H3('Median Market Value'),
            html.P(f"{median_market_value:,.2f}")
        ], style={'width': '24%', 'display': 'inline-block'}),
        html.Div([
            html.H3('Avg. Land Rate'),
            html.P(f"{avg_land_rate:,.2f}")
        ], style={'width': '24%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
    html.Br(),
    html.Div([
        dcc.Graph(
            id='bar-location',
            figure=px.bar(df.groupby('Location')['Market Value'].mean().reset_index(),
                          x='Location', y='Market Value',
                          title='Average Market Value by Location')
        ),
        dcc.Graph(
            id='box-area',
            figure=px.box(df, x='Area', y='Market Value',
                          title='Market Value Distribution by Area')
        ),
    ], style={'display': 'flex', 'gap': '40px'}),
    html.Div([
        dcc.Graph(
            id='histogram-market',
            figure=px.histogram(df, x='Market Value', nbins=20,
                                title='Market Value Distribution')
        ),
        dcc.Graph(
            id='pie-type',
            figure=px.pie(df, names='Property Type',
                          title='Property Type Proportion')
        ),
    ], style={'display': 'flex', 'gap': '40px'}),
    html.H2('Property Data Table'),
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action='native',
        sort_action='native',
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
    )
])

if __name__ == '__main__':
    # Get port and host from environment variables (for deployment)
    port = int(os.environ.get('PORT', 8050))
    app.run(host='0.0.0.0', port=port, debug=False) 