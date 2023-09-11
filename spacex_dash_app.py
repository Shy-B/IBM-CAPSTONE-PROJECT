# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

x = spacex_df["Launch Site"].value_counts().index.to_list()
drop_dict = {}
options_vals = []
for itm in x:
    drop_dict["label"] = itm
    drop_dict["value"] = itm
    options_vals.append(drop_dict.copy())
options_vals.append({'label': 'All Sites', 'value': 'ALL'})
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=options_vals,
                                    value="ALL",
                                    placeholder="select a launch site",
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=min_payload,
                                    max=max_payload,
                                    step=1000,
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names="Launch Site", 
        title='ALL VALUES')
        return fig
    else:
        fig = px.pie(filtered_df[(filtered_df["Launch Site"]==entered_site)], 
        values='class', 
        names="Launch Site", 
        color="class",
        title='Filtered Values')
        return fig
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', 
        y="Launch Site", 
        color="class",
        title='title')
        return fig
    else:
        fig = px.scatter(filtered_df[(filtered_df["Launch Site"]==entered_site)],
        x='Payload Mass (kg)', 
        y="Launch Site",
        color="class", 
        title='title')
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
