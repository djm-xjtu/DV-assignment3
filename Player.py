import pandas as pd

import plotly.graph_objs as pgraph

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcore
import dash_html_components as dhtml

from process import preprocess

data = pd.read_csv('data/data_1000_top_players.csv')
data = preprocess(data)

countries = list(data.Nationality.unique())
external_stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheet)
app.title = 'Assignment3'
optionsName = [{'label': i, 'value': i} for i in data['Name']]
opt = ["Age", "Wage(€ Million)", "Value(€ Million)", "Overall", "Potential", "International Reputation",
       "Height(cm)", "Weight(lbs)", "Release Clause(€ Million)", "Strength"]
options = [{'label': i, 'value': i} for i in opt]
dots = list(range(0, 1001, 50))
app.layout = dhtml.Div([
    dhtml.Div([
        dbc.Row(
            [
                dbc.Col(dhtml.Div([
                    dcore.Dropdown(
                        options=optionsName,
                        searchable=True,
                        value='L. Messi',
                        id='select_name',
                    ),
                ])),
            ],
        ),
        dbc.Card([
            dbc.CardImg(id='player_img', top=True),
            dbc.CardBody([
                dhtml.Img(id='player_national_flag'),
                dhtml.H6(id='player_description_1'),
                dhtml.H6(id='player_description_2')
            ])
        ], style={"padding-top": "20px", "text-align": "center", "width": "100%", 'display': 'inline-block',
                  "background": "white"})
    ]),

    dhtml.Div([
        dcore.Graph(id='player_skill_info_1'),
    ], style={'width': '33.3%', 'display': 'inline-block'}),

    dhtml.Div([
        dcore.Graph(id='player_skill_info_2'),
    ], style={'width': '33.3%', 'display': 'inline-block'}),

    dhtml.Div([
        dcore.Graph(id='player_skill_info_3'),
    ], style={'width': '33.3%', 'display': 'inline-block'}),

    dhtml.P([
        dcore.Dropdown(
            options=options,
            value='Age',
            searchable=False,
            id='x_label',
            style={'width': '500px',
                   'fontSize': '15px',
                   'color': 'black',
                   'display': 'inline-block'
                   }
        ),

        dcore.Dropdown(
            options=options,
            value='Wage(€ Million)',
            searchable=False,
            id='y_label',
            style={'width': '500px',
                   'fontSize': '15px',
                   'color': 'black',
                   'padding-left': '4%',
                   'display': 'inline-block'
                   }
        )
    ], style={'width': '100%', 'display': 'inline-block', 'text-align': 'center', 'padding': '0 20'}),

    dhtml.Div([
        dcore.Graph(
            id='player_figure',
            hoverData={'points': [{'text': 'Cristiano Ronaldo'}]},
        ),

        dcore.Slider(
            id='player_number',
            min=min(dots),
            max=max(dots),
            value=250,
            step=None,
            marks={str(count): str(count) for count in dots},
        ),

    ]),

])


# @app.callback(
#     dash.dependencies.Output('player_name', 'children'),
#     [dash.dependencies.Input('select_name', 'value')],
# )
# def getName(select_name):
#     return select_name


@app.callback(
    dash.dependencies.Output('player_national_flag', 'src'),
    [dash.dependencies.Input('select_name', 'value')],
)
def getNationalFlag(select_name):
    photoURL = data[data['Name'] == select_name]['Flag'].values[0]
    image = photoURL.split('/')[-1]
    return app.get_asset_url('top_1000_flags/' + image)


@app.callback(
    dash.dependencies.Output('player_img', 'src'),
    [dash.dependencies.Input('select_name', 'value')],
)
def getPlayerImg(select_name):
    photoURL = data[data['Name'] == select_name]['Photo'].values[0]
    image = photoURL.split('/')[-1]
    return app.get_asset_url('top_1000_players/' + image)


@app.callback(
    dash.dependencies.Output('player_description_1', 'children'),
    [dash.dependencies.Input('select_name', 'value')],
)
def getPlayerDescription_1(select_name):
    row = data[data['Name'] == select_name]
    age = row['Age'].values[0]
    nation = row['Nationality'].values[0]
    club = row['Club'].values[0]
    height = row['Height'].values[0]
    weight = row['Weight'].values[0]
    description = "Name: {}   |   Age: {}   |   Nationality: {}   |   Club: {}   |   Height: {}cm   |   Weight: {}lbs".format(
        str(select_name), str(age),
        str(nation), str(club), str(height), str(weight))
    return description


@app.callback(
    dash.dependencies.Output('player_description_2', 'children'),
    [dash.dependencies.Input('select_name', 'value')],
)
def getPlayerDescription_2(select_name):
    row = data[data['Name'] == select_name]
    overall = row['Overall'].values[0]
    potential = row['Potential'].values[0]
    wage = row['Wage'].values[0]
    value = row['Value'].values[0]
    description = "Overall Rating: {}  |  Potential: {}  |  " \
                  "Wage: €{}Million   |  Value: €{}Million ".format(str(overall), str(potential), str(wage), str(value))
    return description


@app.callback(
    dash.dependencies.Output('player_skill_info_1', 'figure'),
    [dash.dependencies.Input('select_name', 'value')])
def renderPlayerSkillInfo_1(select_name):
    row = data[data['Name'] == select_name]
    cols = ['Crossing', 'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys', 'Dribbling',
            'Curve', 'FKAccuracy', 'LongPassing', 'BallControl', 'Acceleration',
            'SprintSpeed', 'Agility', 'Reactions', 'Balance', 'ShotPower',
            'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression',
            'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure',
            'Marking', 'StandingTackle', 'SlidingTackle']
    info = row[cols]

    trace = pgraph.Scatterpolar(r=info.values.tolist()[0],
                                theta=cols,
                                name='Attributes',
                                fill='toself',
                                line=dict(color='blue')
                                )

    layout = pgraph.Layout(title=dict(text='Attributes', font=dict(size=15)),
                           font_size=10,
                           height=400,
                           margin={'l': 0, 'b': 30, 't': 70, 'r': 0},
                           hovermode='closest',
                           polar=dict(
                               radialaxis=dict(
                                   visible=True,
                                   range=[0, 100]
                               )
                           ),
                           showlegend=True,
                           )
    fig = pgraph.Figure(data=[trace], layout=layout)
    return fig


@app.callback(
    dash.dependencies.Output('player_skill_info_2', 'figure'),
    [dash.dependencies.Input('select_name', 'value')])
def renderPlayerSkillInfo_2(select_name):
    cols = ['LS', 'ST', 'RS', 'LW', 'LF', 'CF', 'RF', 'RW',
            'LAM', 'CAM', 'RAM', 'LM', 'LCM', 'CM', 'RCM', 'RM', 'LWB', 'LDM',
            'CDM', 'RDM', 'RWB', 'LB', 'LCB', 'CB', 'RCB', 'RB']
    row = data[data['Name'] == select_name]
    info = row[cols]

    trace = pgraph.Scatterpolar(r=info.values.tolist()[0],
                                theta=cols,
                                name='Skills',
                                fill='toself',
                                line=dict(color='green')
                                )
    layout = pgraph.Layout(title=dict(text='Skills', font=dict(size=15)),
                           font_size=10,
                           height=400,
                           margin={'l': 0, 'b': 30, 't': 70, 'r': 0},
                           hovermode='closest',
                           polar=dict(
                               radialaxis=dict(
                                   visible=True,
                                   range=[0, 100]
                               )
                           ),
                           showlegend=True,
                           )
    fig = pgraph.Figure(data=[trace], layout=layout)
    return fig


@app.callback(
    dash.dependencies.Output('player_skill_info_3', 'figure'),
    [dash.dependencies.Input('select_name', 'value')])
def renderPlayerSkillInfo_3(select_name):
    row = data[data['Name'] == select_name]
    cols = ['GKDiving', 'GKHandling',
            'GKKicking', 'GKPositioning', 'GKReflexes']
    info = row[cols]

    trace = pgraph.Scatterpolar(r=info.values.tolist()[0],
                                theta=cols,
                                name='Goalkeeping',
                                fill='toself',
                                line=dict(color='red')
                                )
    layout = pgraph.Layout(title=dict(text='Goalkeeping', font=dict(size=15)),
                           font_size=10,
                           height=400,
                           margin={'l': 0, 'b': 30, 't': 70, 'r': 0},
                           hovermode='closest',
                           polar=dict(
                               radialaxis=dict(
                                   visible=True,
                                   range=[0, 100]
                               )
                           ),
                           showlegend=True,
                           )
    fig = pgraph.Figure(data=[trace], layout=layout)
    return fig


@app.callback(
    dash.dependencies.Output('player_figure', 'figure'),
    [dash.dependencies.Input('x_label', 'value'),
     dash.dependencies.Input('y_label', 'value'),
     dash.dependencies.Input('player_number', 'value')]
)
def getTwoAttributeFigure(x_label, y_label, player_number):
    rows = data[:player_number]
    trace = [
        dict(
            x=rows[rows['Nationality'] == i][x_label].sort_values(ascending=False),
            y=rows[rows['Nationality'] == i][y_label].sort_values(ascending=True),
            text=rows[rows['Nationality'] == i]['Name'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ) for i in rows.Nationality.unique()
    ]
    layout = dict(
        title={"text": str(player_number) + " FIFA 2022 players\' " + str(x_label) + " compares to " + str(y_label),
               "font": {"size": 15}},
        xaxis={'type': 'linear', 'title': x_label},
        yaxis={'title': y_label},
        title_x=0.5,
        margin={'l': 40, 'b': 40, 't': 60, 'r': 10},
        legend={'x': 1, 'y': 0},
        hovermode='closest',
        height=490,
    )
    fig = pgraph.Figure(data=trace, layout=layout)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8082)
