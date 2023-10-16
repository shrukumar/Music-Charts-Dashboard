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
        value='',
   ),


   dcc.Graph(id="graph")


])


@app.callback(
   Output("graph", "figure"),
   Input("input", "value")
)

def input_song(name):


   df = pd.read_csv('spotify-2023.csv')


   keys = df['track_name'].values
   keys_list = list(keys)


   if name in keys_list:

       filtered_df = df.loc[df['track_name'] == f'{name}']

       # Get the row index associated with the key in the 'Name' column
       row_index = filtered_df.index[0]

       song_dict = {'Spotify': df.iloc[row_index]['in_spotify_charts'],
                    'Apple' :df.iloc[row_index]['in_apple_charts'],
                    'Deezer' :df.iloc[row_index]['in_deezer_charts'],
                    'Shazam' :df.iloc[row_index]['in_shazam_charts'] }


       # change data types of chart values into integers
       int_values = [int(value) for value in song_dict.values()]


       platforms = list(song_dict.keys())
       charts = int_values


       # creation of bar plot
       fig = px.bar(x=platforms, y=charts)
       fig.update_layout(title = 'Rankings of Streaming Services', xaxis_title='Platforms', yaxis_title='Charts')

       return fig

# step 4: Run the server
app.run_server(debug=True)
