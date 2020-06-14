import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from pymongo import MongoClient
import plotly.graph_objs as go
import random
username='ENTER YOUR ATLAS MONGO CREDENTIALS HERE'
password='ENTER YOUR ATLAS MONGO CREDENTIALS HERE'
client = MongoClient("mongodb+srv://"+username +':' + password + "@project-rhxmt.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database("gameweek")
records = db['finalgw']
cumrecords = db.cumulative
app = dash.Dash(__name__)
df = pd.read_csv(r'D:\Allen Stuff/Project\Dash/cumulative.csv', encoding='latin1')
players = pd.read_csv(r'gws/gw1.csv', encoding='latin1')
valuelist = list(players.columns.values)
available_indicators = list(df.columns.values)

teamlist = ['Arsenal', 'Bournemouth', 'Brighton', 'Burnley', 'Cardiff', 'Chelsea', 'Crystal Palace', 'Everton',
            'Fulham', 'Huddersfield', 'Leicester', 'Liverpool', 'Manchester City', 'Manchester United',
            'Newcastle United', 'Southampton', 'Tottenham Hotspurs', 'Watford', 'West Ham', 'Wolves']
app.title = 'PL Statistics'
app.layout = html.Div(style={'backgroundColor': "#111111"}, children=[
    html.Div([
        html.Div([html.Img(src='assets/246x0w.jpg',
                           height='200px')], style={'float': 'left', 'width': '10%'}),
        html.P(html.B("Premier League Statistics 2018-2019"))
    ], style={'textAlign': 'center', 'background': '#00FF87', 'color': '#340D39', 'fontSize': '70px', 'height': '200px',
              'width': '2079px', 'padding': '10px', 'fontFamily': 'Verdana'}),

    html.Div([
        dcc.Dropdown(
            id='crossfilter-xaxis-column',
            options=[{'label': i.replace('_', ' ').title(), 'value': i} for i in available_indicators],
            value='minutes'
        ),

        dcc.Dropdown(
            id='crossfilter-yaxis-column',
            options=[{'label': i.replace('_', ' ').title(), 'value': i} for i in available_indicators],
            value='goals_scored'
        )
    ], style={'width': '10%'}),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            selectedData={'points': [{'text': 'Anthony Martial'}]}
        )
    ], style={'width': '100%', 'display': 'inline-block'}),
    html.Div(
        dcc.Dropdown(
            id='crossfilter_tr_column',
            options=[{'label': q.replace('_', ' ').title(), 'value': q} for q in valuelist],
            value='goals_scored',
        ), style={'width': '10%', 'backgroundColor': '#111111'}),
    html.Div([
        html.Div(
            dcc.Graph(id='multiselect',
                      hoverData={'points': [{'text': 'Anthony Martial'}]},
                      clickData={'points': [{'text': 'Anthony Martial'}]}
                      )
            , style={'display': 'inline-block', 'width': '50%', 'float': 'left'}),

        html.Div(
            dcc.Graph(id='teamform', clickData={'points': [{'curveNumber': 0, 'pointNumber': 14, 'pointIndex': 14, 'x': 14, 'y': 2, 'text': 'Manchester United v/s Arsenal<br>05 Dec 20:00'}]})
            , style={'display': 'inline-block', 'width': '50%', 'float': 'left'}),
    ]),
		html.Div([
			
				
					html.Div([
					html.Br(),
						dcc.Dropdown(
							id='team-dropdown1',
							options=[{'label': team, 'value': team} for team in teamlist],
							value='Arsenal'
						),
						dcc.Dropdown(
							id='opt-dropdown1',
							value='Alexandre Lacazette'
						),
						dcc.Dropdown(
							id='team-dropdown2',
							options=[{'label': team, 'value': team} for team in teamlist],
							value='Manchester United'

						),
						dcc.Dropdown(
							id='opt-dropdown2',
							value='Anthony Martial'

						)], style={'width': '20%'}),
					dcc.Graph(id='radar1')
				
    ,
                  html.Div([
                      html.Div(html.Img(id='hometeamimage',style={'height':'200px','display':'block','float':'centre','margin':'auto'}),style={'display':'inline-block','width':'50%','float':'left'}),
                      html.Div(html.Img(id='awayteamimage',style={'height':'200px','display':'block','float':'centre','margin':'auto'}),style={'display':'inline-block','width':'50%','float':'right'})]),
                  dash_table.DataTable(id='matchdata',
                                       columns=[
                                           {'name': 'Home', 'id': 'Home'},
                                           {'name': 'Away', 'id': 'Away'}
                                       ],
                                       style_header={
                                           'backgroundColor': '#111111', 'fontWeight': 'bold', 'fontSize': '0px',
                                           'border': '1px black'
                                       },
                                       style_data_conditional=[
                                           {
                                               'if': {'row_index': 'odd'},
                                               'backgroundColor': '#6b6b6b'
                                           },

                                       ],
                                       style_cell_conditional=[
                                           {'if': {'column_id': 'Home'},
                                            'width': '50%'},
                                           {'if': {'column_id': 'Away'},
                                            'width': '50%'},
                                       ],
                                       style_table={
                                           'height': '392px',

                                       },
                                       style_cell={
                                           'backgroundColor': '#111111',
                                           'color': 'white',
                                           'textAlign': 'center',
                                           'border': '1px black'
                                       }, style_as_list_view=True
                                       ),
                  ], style={'backgroundColor': '#111111', 'width': '100%'})])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name):
    traces = []
    dff = df
    for i in teamlist:
        df_by_team = dff[dff['team'] == i]
        traces.append(go.Scatter(
            x=df_by_team[xaxis_column_name],
            y=df_by_team[yaxis_column_name],
            text=df_by_team['name'],
            customdata=df_by_team['name'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': (15 * df_by_team[yaxis_column_name] / df[yaxis_column_name].max() + 5),
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))
    return {
        'data': traces,
        'layout': go.Layout(
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest',
            template='plotly_dark',
            clickmode='event+select'

        )
    }


@app.callback(
    dash.dependencies.Output('multiselect', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'selectedData'),
     dash.dependencies.Input('crossfilter_tr_column', 'value')])
def update_x_timeseries(selectedData, crossfilter_tr_column):
    selectedplayers = pd.DataFrame(selectedData.get('points'))
    gwdata = pd.DataFrame()
    for names in selectedplayers.text:
        gwdata = gwdata.append(pd.DataFrame(records.find({"name": names})))
    traces = []
    for i in gwdata.name.unique():
        df_by_name = gwdata[gwdata['name'] == i]
        traces.append(go.Scatter(
            x=df_by_name['round'],
            y=np.cumsum(df_by_name[crossfilter_tr_column]),
            text=df_by_name['name'],
            mode='lines+markers',
            opacity=0.7,
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest',
            template='plotly_dark'

        )
    }


@app.callback(
    dash.dependencies.Output('teamform', 'figure'),
    [dash.dependencies.Input('multiselect', 'clickData')])
def update_x_timeseries(hoverData):
    selectedplayers = pd.DataFrame(hoverData.get('points', 'color'))
    gwdata = pd.DataFrame()
    for names in selectedplayers.text:
        gwdata = gwdata.append(
            pd.DataFrame(records.find({"name": names},
                                      {'kickoff_time_formatted', 'oteam', 'team', 'team_a_score', 'team_h_score',
                                       'was_home'})))
    gwdata['score'] = gwdata[gwdata['was_home']]['team_h_score']
    gwdata['score'] = gwdata['score'].fillna(gwdata['team_a_score'])
    gwdata['oppscore'] = gwdata[gwdata['was_home'] == False]['team_h_score']
    gwdata['oppscore'] = gwdata['oppscore'].fillna(gwdata['team_a_score'])

    ################

    ################

    traces = []
    gwlist = list(range(0, 38))
    traces.append(go.Bar(
        x=gwlist,
        y=gwdata['score'] + 0.05,
        name=gwdata['team'][0],
        text=gwdata['team'][0] + str(' v/s ') + gwdata['oteam'][gwlist] + '<br>'
             + gwdata['kickoff_time_formatted'][gwlist],
        hoverinfo='text',
        marker_color='#00aa55'

    ))
    traces.append(go.Bar(
        x=gwlist,
        y=-gwdata['oppscore']-0.05,
        name='Opponent Teams',
        text=gwdata['oteam'][gwlist],
        hoverinfo='text',
    ))

    return {
        'data': traces,
        'layout': go.Layout(
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest',
            template='plotly_dark',
            barmode='relative'

        )
    }


@app.callback(
    dash.dependencies.Output('opt-dropdown1', 'options'),
    [dash.dependencies.Input('team-dropdown1', 'value')]
)
def name_dropdown(value):
    playerdf = pd.DataFrame()
    playerdf = playerdf.append(
        pd.DataFrame(cumrecords.find({"team": value},
                                     {'name'})))

    return [{'label': i, 'value': i} for i in playerdf['name']]


@app.callback(
    dash.dependencies.Output('opt-dropdown2', 'options'),
    [dash.dependencies.Input('team-dropdown2', 'value')]
)
def name_dropdown(value):
    playerdf = pd.DataFrame()
    playerdf = playerdf.append(
        pd.DataFrame(cumrecords.find({"team": value},
                                     {'name'})))

    return [{'label': i, 'value': i} for i in playerdf['name']]


@app.callback(
    dash.dependencies.Output('radar1', 'figure'),
    [dash.dependencies.Input('opt-dropdown1', 'value'),
     dash.dependencies.Input('opt-dropdown2', 'value')])
def update_x_timeseries(name1, name2):
    templist = list
    traces = []
    names = [name1, name2]
    for name in names:
        gwdata = pd.DataFrame()
        gwdata = gwdata.append(
            pd.DataFrame(cumrecords.find({"name": name},
                                         {'assists', 'goals_scored', 'big_chances_created',
                                          'clean_sheets', 'completed_passes'
                                          })))

        gwdata['completed_passes'] = gwdata['completed_passes'] / 90
        for index, rows in gwdata.iterrows():
            templist = [rows.assists, rows.big_chances_created, rows.clean_sheets, rows.completed_passes,
                        rows.goals_scored]

        gwlist = ['Assists', 'Big Chances Created', 'Clean Sheets', 'Completed Passes / 90 Minutes', 'Goals Scored', ]
        traces.append(go.Scatterpolar(
            r=templist,
            theta=gwlist,
            fill='toself',
            name=name

        ))

    return {
        'data': traces,
        'layout': go.Layout(
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest',
            template='plotly_dark'

        )
    }


@app.callback(
    [dash.dependencies.Output('matchdata', 'data'),
     dash.dependencies.Output('hometeamimage', 'src'),
     dash.dependencies.Output('awayteamimage', 'src')],
    [dash.dependencies.Input('teamform', 'clickData')])
def update_x_timeseries(clickData):
    selectedmatch = pd.DataFrame(clickData.get('points'))
    data = pd.DataFrame()
    new = selectedmatch['text'].str.split("v/s", n=1, expand=True)
    data['team'] = new[0].str.strip()
    teamname = str(data.iloc[0, 0])
    gwdf = pd.DataFrame()
    gwdf['Match'] = selectedmatch['x']
    fixtures = db['fixtures']
    gwdata = pd.DataFrame()
    gwdata = gwdata.append(
        pd.DataFrame(fixtures.find({"HomeTeam": teamname, "Match": gwdf['Match'][0].item() + 1})))
    gwdata = gwdata.append(
        pd.DataFrame(fixtures.find({"AwayTeam": teamname, "Match": gwdf['Match'][0].item() + 1})))
    gwdata = gwdata.drop(columns='_id')
    gwdata = gwdata.drop_duplicates()
    returnlist = stattable(gwdata)
    datadf = returnlist[0]
    tempdf = returnlist[1]
    data = datadf.to_dict('records')
    return [data,r'assets/'+tempdf.iloc[0]['Home'],r'assets/'+tempdf.iloc[0]['Away']]


def namecleaner(namedf):
    namedf['name'] = namedf['name'].str.replace("_", " ")
    namedf['name'] = namedf['name'].str.replace('\d+', "")
    namedf['name'] = namedf['name'].str.strip()
    return namedf


# ************************************************BEAUTIFUL 10/10 CODE************************************* #
def stattable(statdf):
    newdf = pd.DataFrame(columns=['Home', 'Away'])
    c = int(0)
    for x in ['H', 'A']:
        for y in ['FT' + str(x) + 'G', str(x) + 'S', str(x) + 'ST', str(x) + 'F', str(x) + 'C', str(x) + 'Y',
                  str(x) + 'R']:
            temp = statdf.iloc[0][y]
            pytemp = temp.item()
            if x == 'H':
                col = 'Home'
            else:
                col = 'Away'
            newdf.at[c, col]=pytemp
            c = c + 1
        c = 0
    tempdf = pd.DataFrame(columns=['Home', 'Away'])
    imgdf = pd.DataFrame(columns=['Home', 'Away'])
    temp = statdf.iloc[0]['HomeTeam']
    tempdf.at[0, 'Home'] = temp
    imgdf.at[0, 'Home']= temp +'.svg'
    temp = statdf.iloc[0]['AwayTeam']
    tempdf.at[0, 'Away'] = temp
    imgdf.at[0, 'Away']= temp + '.svg'
    newdf = tempdf.append(newdf)
    return newdf,imgdf


# @app.callback(
#     [dash.dependencies.Output('hometeamimage', 'src'),
#      dash.dependencies.Output('awayteamimage', 'src')],
#     [dash.dependencies.Input('teamform', 'clickData')])
# def update_x_timeseries(clickData):
#     return [r'assets/Watford.svg', r'assets/Watford.svg']


# ************************************************BEAUTIFUL 10/10 CODE************************************* #

if __name__ == '__main__':
    app.run_server(debug=True)
