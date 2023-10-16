from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd


# step 1: define the app object
app = Dash(__name__)


# step 2: define the layout
   app.layout = html.Div([
       html.H4('Songs in Playlists vs Song Rankings'),
       html.P('Select Streaming Platform:'),
       dcc.Dropdown(
           id="dropdown",
           options=['apple', 'deezer','spotify'],
           value='apple',
           clearable=False
       ),
       dcc.Graph(id="graph")


   ])



# step 3: Define the callback which triggers visualization updates in response to changing the control settings


@app.callback(
    Output("graph", "figure"),
    Input("dropdown", "value")
)




def rank_vis(platform):
    """
    Creates a scatter plot of the number of songs in playlists and how they
    rank in the charts based on the platform input
    :param platform: string that indicates platform
    :return: plot
    """
    df = pd.read_csv('spotify-2023.csv')
    plot = px.scatter(df, x=f'in_{platform}_playlists', y=f'in_{platform}_charts', hover_data=['track_name'])


    plot.update_layout(title=f'{platform} Playlists vs Rankings', xaxis_title='Number of Playlists',
                       yaxis_title='Rankings', hovermode='closest')


    return plot




# step 4: Run the server
app.run_server(debug=True)
