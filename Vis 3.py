from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd


# step 1: define the app object
app = Dash(__name__)


# step 2: define the layout
app.layout = html.Div([
   html.H4('Check Song Rankings'),
   html.P('Enter Song Name :'),

    # dcc.Dropdown(
    #     id="dropdown",
    #     options=['Die For You', 'Lucid Dreams', 'Rush'],
    #     value='Rush',
    #     clearable=False
    dcc.Input(
        id='input',
        placeholder='Enter text...',
        type='text',
        value = ''

   ),


   dcc.Graph(id="graph")


])


@app.callback(
   Output("graph", "figure"),
   Input("input", "value")
)
def input_song(name):
    df = pd.read_csv('test.csv')

    keys = list(df['track_name'])

    if name in keys:
        df = df.loc[df['track_name'] == f'{name}']
        song_dict = {'Spotify': df.iloc[0]['in_spotify_charts'],
                     'Apple': df.iloc[0]['in_apple_charts'],
                     'Deezer': df.iloc[0]['in_deezer_charts'],
                     'Shazam': df.iloc[0]['in_shazam_charts']}

        fig = px.bar(x=song_dict.keys(), y=song_dict.values())
        fig.update_layout(title='Rankings of Streaming Services', xaxis_title='Platforms', yaxis_title='Charts')

    else:
        fig = px.scatter(x=0, y=0)
        fig.update_layout(title='Song not in Database. Enter another song.')

    return fig



# step 4: Run the server
app.run_server(debug=True)
