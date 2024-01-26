# Import packages
from dash import Dash, html, dash_table,dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Incorporate data
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
#df = pd.read_csv('baseballpower.csv')
df = pd.read_csv('baseballrankings2023.csv')
dfrank = df.copy()

playmeans = {'H9': 6.134250750678779,
 'BB9': 2.4275243199108396,
 '2B-A9': 0.5713381443873534,
 '3B-A9': 0.1372064098537924,
 'HR-A9': 1.0781937789990343,
 'SO9': -1.1741945886916918,
 'SHA9': 0.052945139523348415,
 'SFA9': 0.3180772421109358,
 'GO9': -1.1220360675354708,
 'FO9': -1.3377788350519717,
 'RBI9': 0.04393702811812265,
 'runs_allowed9': 7.129463322303073}


playweights = {'H': 0.6122493552221964,
 'BB': 0.5104905202349009,
 '2B-A': 0.29504139443334726,
 '3B-A': 0.6096058517722156,
 'HR-A': 0.8974012298455808,
 'SO': -0.13947783499634106,
 'SHA': 0.12970816945321836,
 'SFA': 0.6999609385053032,
 'GO': -0.13633278134761573,
 'FO': -0.14780528616709124,
 'runs_allowed': 1}

usecols = ['ncaa_name','H9_x', 'BB9_x', '2B-A9_x', '3B-A9_x', 'HR-A9_x', 'SO9_x','SHA9_x', 'SFA9_x', 'GO9_x', 'FO9_x', 'RBI9_x', 'HitValue', 'H9_y', 'BB9_y', '2B-A9_y', '3B-A9_y','HR-A9_y', 'SO9_y', 'SHA9_y', 'SFA9_y', 'GO9_y', 'FO9_y', 'RBI9_y','PitchValue', 'NetValue']

#Round
df[['H9_x', 'BB9_x', '2B-A9_x', '3B-A9_x', 'HR-A9_x', 'SO9_x',
       'SHA9_x', 'SFA9_x', 'GO9_x', 'FO9_x', 'RBI9_x', 'HitValue',
        'H9_y', 'BB9_y', '2B-A9_y', '3B-A9_y',
       'HR-A9_y', 'SO9_y', 'SHA9_y', 'SFA9_y', 'GO9_y', 'FO9_y', 'RBI9_y',
       'PitchValue', 'NetValue']]=df[['H9_x', 'BB9_x', '2B-A9_x', '3B-A9_x', 'HR-A9_x', 'SO9_x',
       'SHA9_x', 'SFA9_x', 'GO9_x', 'FO9_x', 'RBI9_x', 'HitValue',
        'H9_y', 'BB9_y', '2B-A9_y', '3B-A9_y',
       'HR-A9_y', 'SO9_y', 'SHA9_y', 'SFA9_y', 'GO9_y', 'FO9_y', 'RBI9_y',
       'PitchValue', 'NetValue']].round(2)

for c in ['H9_x','BB9_x', '2B-A9_x', '3B-A9_x', 'HR-A9_x', 'SO9_x', 'SHA9_x', 'SFA9_x','GO9_x', 'FO9_x', 'RBI9_x', 'HitValue','NetValue']:
    dfrank[c]=dfrank.groupby("RankDate")[c].rank(ascending=False)

for c in ['H9_y', 'BB9_y', '2B-A9_y', '3B-A9_y', 'HR-A9_y', 'SO9_y','SHA9_y', 'SFA9_y', 'GO9_y', 'FO9_y', 'RBI9_y', 'PitchValue']:
     dfrank[c]=dfrank.groupby("RankDate")[c].rank(ascending=True)  



# Initialize the app
app = Dash(__name__)
server = app.server

# App layout
app.layout = html.Div([
    html.H2(children='College Baseball Performance Ratings'),
    dcc.Dropdown(id='dates', value=df['RankDate'].max(),clearable=False, options=[{'label':i,'value':i} for i in df['RankDate'].unique()]),
    dcc.RadioItems(['Full','Simple','Ranking'],'Full',inline=True,id='tabletype'),
    dcc.Dropdown(id='teamdropdown',
    options=[{'label':i,'value':i} for i in df['ncaa_name'].unique()],
    placeholder="Select A Team"
                ),
    dcc.Dropdown(id='teamdropdown2',
    options=[{'label':i,'value':i} for i in df['ncaa_name'].unique()],
                 placeholder="Select A Team"
                ),
    dash_table.DataTable(
        id='rankingtable', sort_action='native', page_size=20,
        style_cell_conditional=[{'if': {'column_id':c}, 'backgroundColor':'lightyellow'} for c in ['ncaa_name','HitValue','PitchValue','NetValue']]
                        ),
    
    html.H3(children='Average Adjusted Runs Added:'),
    dash_table.DataTable(id='headtohead'),
    
    
    html.H3(children='Performance Ranking Trend:'),
    dcc.RadioItems(['Overall','Hitting','Pitching'],'Overall',inline=True,id='graphtype'),
    dcc.Graph(id="graph")
])


#Full DataTable
@app.callback(
    Output(component_id='rankingtable',component_property='data'),
    Input(component_id='teamdropdown', component_property='value'),
    Input(component_id='teamdropdown2', component_property='value'),
    Input('tabletype','value'),
    Input(component_id='dates', component_property='value'),
)
def updatetable(teamfilter,teamfilter2,tabletype,selecteddate):
    if tabletype=='Simple':
        cols=['ncaa_name','HitValue','PitchValue','NetValue']
        dfdisplay = df.copy()
    elif tabletype=='Ranking':
        cols=usecols
        dfdisplay = dfrank.copy()
        
    else:
        cols=usecols
        dfdisplay = df.copy()
    
    if (teamfilter==None) & (teamfilter2==None):
        return dfdisplay[dfdisplay['RankDate']==selecteddate][cols].to_dict('records')
    else:
        return dfdisplay[(dfdisplay['ncaa_name'].isin([teamfilter,teamfilter2]) )& (dfdisplay['RankDate']==selecteddate)][cols].to_dict('records')


#HeadtoHead Table
@app.callback(
    Output(component_id='headtohead',component_property='data'),
    Input(component_id='teamdropdown', component_property='value'),
    Input(component_id='teamdropdown2', component_property='value')
)
def updateheadtohead(teamfilter,teamfilter2):
    
    if (teamfilter!=None) & (teamfilter2!=None):
        test = df[(df['ncaa_name'].isin([teamfilter,teamfilter2]))& (df["RankDate"]==df['RankDate'].max())].copy().reset_index()
        for x,y in [(x,x.replace("_x","_y")) for x in ['H9_x', 'BB9_x', '2B-A9_x', '3B-A9_x', 'HR-A9_x', 'SO9_x','SHA9_x', 'SFA9_x', 'GO9_x', 'FO9_x', 'RBI9_x']]:
            test.loc[0,x]=test.loc[0,x]+test.loc[1,y]+playmeans[x.replace("_x","")]
            test.loc[1,x]=test.loc[1,x]+test.loc[0,y]+playmeans[x.replace("_x","")]
        
        test.loc[0,'HitValue']=(test.loc[0,'HitValue']+test.loc[1,'PitchValue'])+playmeans['runs_allowed9']
        test.loc[1,'HitValue']=(test.loc[1,'HitValue']+test.loc[0,'PitchValue'])+playmeans['runs_allowed9']
        
        test = test[['ncaa_name',#'school_id',
                'H9_x', 'BB9_x', '2B-A9_x', '3B-A9_x', 'HR-A9_x', 'SO9_x',
               'SHA9_x', 'SFA9_x', 'GO9_x', 'FO9_x', 'RBI9_x','HitValue']].round(1)
        test.columns=[x.replace("9_x","") for x in test.columns]

        return test.rename(columns={'HitValue':'Expected Runs'}).to_dict('records')
    else:
        return None



#Chart
@app.callback(
    Output("graph", "figure"),
    Input(component_id='teamdropdown', component_property='value'),
    Input(component_id='teamdropdown2', component_property='value'),
    Input(component_id='graphtype', component_property='value'),
)
def display_color(team,team2,graphtype):
    #fig = go.Figure(go.Bar(x=x, y=[2, 3, 1], marker_color='red'))
    #fig = go.Figure()
    if graphtype=='Overall':
        y='Margin vs Average Opponent'#'NetValue'
    elif graphtype=='Hitting':
        y='Runs Above Average'
    elif graphtype=='Pitching':
        y='Runs Allowed Above Average'
    
    fig = px.line(df[df["ncaa_name"].isin([team,team2])].rename(columns={'HitValue':'Runs Above Average','PitchValue':'Runs Allowed Above Average','NetValue':'Margin vs Average Opponent'}),x='RankDate',y=y, color="ncaa_name")
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
