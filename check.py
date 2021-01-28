import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#Currently using external CSS/JavaScript
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#------------------------------------------------------------------------------------------
# Getting Michigan Data from CSV
scope = ['Michigan', 'Wisconsin', 'Indiana', 'Ohio', 'Illinois']
data = pd.read_csv("us-counties.csv")
data.fillna(0)
michigan_counties = data[data["state"] == 'Michigan']
ohio_counties = data[data["state"] == 'Ohio']

# Combine Ohio and Michigan variables
test = pd.concat([michigan_counties, ohio_counties], ignore_index=True)

test['date'] = pd.to_datetime(test['date'])
test['day'] = test['date'].dt.day
test['month'] = test['date'].dt.month
test = test.set_index('month')

print(test)

months = np.array([5])

states_data = test.loc[months]
print(states_data)

#Function for getting days
day = 2
bet = states_data[states_data['day'] == day]

print(bet)

# Drop everything but cases and fips
temp = states_data.drop(['county', 'state', 'deaths', 'date'], axis=1)

# Drop all fips with NaN as their value
temp2 = temp.dropna(subset=['fips'])
final_df = temp2.dropna(subset=['cases'])
final_df = final_df.astype(int)

fips = final_df['fips'].tolist()

values = final_df['cases'].tolist()
endpts = list(np.mgrid[min(values):max(values):10j])
colorscale = ['rgb(240,248,255)', 'rgb(230,230,250)', 'rgb(176,224,230)', 'rgb(173,216,230)',
              'rgb(135,206,250)',
              'rgb(135,206,235)', 'rgb(0,191,255)', 'rgb(176,196,222)',
              'rgb(30,144,255)', 'rgb(100,149,237)', 'rgb(70,130,180)']
fig = ff.create_choropleth(
    fips=fips, values=values, scope=scope, show_state_data=True,
    colorscale=colorscale, binning_endpoints=endpts, round_legend_values=True,
    plot_bgcolor='rgb(229,229,229)',
    paper_bgcolor='rgb(229,229,229)',
    legend_title='Cases of COVID-19 In Michigan',
    state_outline={'color': 'rgb(0,0,128)', 'width': 0.1},
    county_outline={'color': 'rgb(0,0,128)', 'width': 0.5},
    exponent_format=True
)

#-------------------------------------------------------------------------------------
app.layout = html.Div([
    html.H1(children='COVID-19 Cases in Michigan'),

    html.Div(children='''
            COVID-19 Cases in Michigan
    '''),

    dcc.Graph(
        id='example_graph', figure=fig
        )
])
#------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)