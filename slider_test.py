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
indiana_counties = data[data["state"] == 'Indiana']

# Combine Ohio and Michigan variables
test = pd.concat([michigan_counties, ohio_counties,indiana_counties], ignore_index=True)

test['date'] = pd.to_datetime(test['date'])
test['day'] = test['date'].dt.day
test['month'] = test['date'].dt.month
test = test.set_index('month')

#-------------------------------------------------------------------------------------
app.layout = html.Div([
    html.H1(children='COVID-19 Cases'),

    html.Div(children='''
            COVID-19 Cases
    '''),

    dcc.Graph(
        id='example_graph'),

    html.Div([
        html.Label(['Choose Month of COVID-19 Cases:'],
                   style={'font-weight': 'bold'}),
        html.P(),
        dcc.Slider(
            id='my_month',  # any name you'd like to give it
            marks={
                1: 'January',  # key=position, value=what you see
                2: 'February',
                3: 'March',
                4: 'April',
                5: 'May',
                6: 'June',
                7: 'July',
                8: 'August',
                9: 'September',
                10: 'October',
                11: 'November',
            },
            step=1,  # number of steps between values
            min=1,
            max=11,
            value=3,  # default value initially chosen
        ),
    ]),
    html.Div([
        html.P(
        ),
        html.Label(['Choose Day of COVID-19 Cases:'],
                   style={'font-weight': 'bold'}),
        html.P(),
        dcc.Slider(
            id='my_day',  # any name you'd like to give it
            marks={
                1: '1',  # key=position, value=what you see
                2: '2',
                3: '3',
                4: '4',
                5: '5',
                6: '6',
                7: '7',
                8: '8',
                9: '9',
                10: '10',
                11: '11',
                12: '12',
                13: '13',
                14: '14',
                15: '15',
                16: '16',
                17: '17',
                18: '18',
                19: '19',
                20: '20',
                21: '21',
                22: '22',
                23: '23',
                24: '24',
                25: '25',
                26: '26',
                27: '27',
                28: '28',
                29: '29',
                30: '30',
                31: '31',
            },
            step=1,  # number of steps between values
            min=1,
            max=31,
            value=25,  # default value initially chosen
        ),
    ]),
])
#------------------------------------------------------------------------------
@app.callback(
    Output(component_id='example_graph', component_property='figure'),
    [Input(component_id='my_month', component_property='value'),
     Input(component_id='my_day', component_property='value')]
)

def update_graph(month, day):
    states_data = test.loc[month]

    states_data = states_data[states_data['day'] == day]

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
    return fig
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)