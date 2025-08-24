import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import numpy as np

# -----------------------------
# Load dataset
# -----------------------------
# Make sure you have spacex_launch_dash.csv in same folder
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# App Setup
app = dash.Dash(__name__)

# -----------------------------
# Layout
# -----------------------------
app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard", style={'textAlign': 'center'}),

    # Dropdown for Launch Sites
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] + 
                [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True,
        style={'width': '60%', 'margin': 'auto'}
    ),

    html.Br(),

    # Pie Chart
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    # Range Slider for Payload Mass
    html.P("Payload Range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={i: f"{i}" for i in range(0, 10001, 2000)},
        value=[0, 10000]
    ),

    html.Br(),

    # Scatter Plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# -----------------------------
# Callbacks
# -----------------------------

# Pie Chart Callback
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Count successes at all sites
        df_all = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(df_all,
                     names='Launch Site',
                     title="Total Successful Launches by Site",
                     hole=0.3)
        fig.update_traces(textinfo='percent+label')
    else:
        # Outcomes for one site
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        outcome_counts = site_data['class'].value_counts().reset_index()
        outcome_counts.columns = ['Outcome', 'Count']
        outcome_counts['Outcome'] = outcome_counts['Outcome'].replace({1: 'Success', 0: 'Failure'})
        fig = px.pie(outcome_counts,
                     names='Outcome', values='Count',
                     title=f"Launch Outcomes at {selected_site}",
                     color='Outcome',
                     color_discrete_map={'Success':'green','Failure':'red'},
                     hole=0.3)
        fig.update_traces(textinfo='percent+label')
    return fig

# Scatter Plot (Payload vs. Success) with trendlines per booster
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range
    # filter by payload range
    df_filtered = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                            (spacex_df['Payload Mass (kg)'] <= high)]
    if selected_site != 'ALL':
        df_filtered = df_filtered[df_filtered['Launch Site'] == selected_site]

    # Base scatter
    fig = px.scatter(
        df_filtered,
        x='Payload Mass (kg)', y='class',
        color='Booster Version Category',
        title=f"Payload vs Launch Outcomes - {selected_site}",
        labels={'class': 'Launch Outcome (0=Failure, 1=Success)'},
        hover_data=['Launch Site']
    )

    # Add success rate lines (in bins)
    bins = np.arange(0, 11000, 2000)   # payload bins of 2000 kg
    df_filtered['Payload Bin'] = pd.cut(df_filtered['Payload Mass (kg)'], bins)

    success_rates = df_filtered.groupby(
        ['Booster Version Category', 'Payload Bin']
    )['class'].mean().reset_index()

    success_rates['Payload Mid'] = success_rates['Payload Bin'].apply(lambda b: b.mid)

    # Add one dashed line per booster category
    for booster in success_rates['Booster Version Category'].unique():
        booster_data = success_rates[success_rates['Booster Version Category'] == booster]
        fig.add_scatter(
            x=booster_data['Payload Mid'],
            y=booster_data['class'],
            mode='lines+markers',
            name=f"Success Rate ({booster})",
            line=dict(width=3, dash='dash')
        )

    return fig

# -----------------------------
# Run the app
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True, port=8051)
    