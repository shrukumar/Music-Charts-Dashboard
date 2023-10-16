from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from datetime import datetime

def rank_vis(df, platform):
    """
    Creates a scatter plot of the number of songs in playlists and how they
    rank in the charts based on the platform input
    :param platform: string that indicates platform
    :return: plot
    """
    for idx in df.index:
        if df.loc[idx][f'in_{platform}_charts'] == 0:
            df = df.drop(idx)


    plot = px.scatter(df, x=f'in_{platform}_playlists', y=f'in_{platform}_charts', hover_data=['track_name'])


    plot.update_layout(title=f'{platform} Playlists vs Rankings', xaxis_title='Number of Playlists',
                       yaxis_title='Rankings', hovermode='closest')


    return plot
def create_hist(df, day_or_month, month_range):
    """
    creates histogram with data about song release dates, can be viewed in months or days and customizable range
    Args:
        day_or_month (str): string indicating to create hist with month or day info
        month_range (ls): list with range of months to limit graph
    Returns:
         fig (plotly.histogram): histogram with song release data
    """

    # dict to map release month int to shortened names
    month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
                  9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

    months = []
    dates = []

    for idx in df.index:
        # finding release month for all rows
        month_int = int(df['released_month'][idx])
        # only appending data if within designated range
        if month_int in range(month_range[0]+1, month_range[1]+2):
            month_str = month_dict[month_int]
            date = month_str + ' ' + str(int(df['released_day'][idx]))

            months.append(month_str)
            dates.append(date)

            # sorting data in chronological order
            months.sort(key=lambda date: datetime.strptime(date, "%b"))
            dates.sort(key=lambda date: datetime.strptime(date, "%b %d"))

    # creating different histograms based on month or day view
    if day_or_month == 'Months':
        fig = px.histogram(x=months)
        fig.update_layout(xaxis_title='Month', yaxis_title='Number of Songs Released')
    if day_or_month == 'Days':
        fig = px.histogram(x=dates)
        fig.update_layout(xaxis_title='Dates', yaxis_title='Number of Songs Released')

    return fig

def input_song(df, name):

   # df = pd.read_csv('test.csv')

   keys = list(df['track_name'])

   if name in keys:
       df = df.loc[df['track_name'] == f'{name}']

   song_dict = {'Spotify': df.iloc[0]['in_spotify_charts'],
                'Apple': df.iloc[0]['in_apple_charts'],
                'Deezer': df.iloc[0]['in_deezer_charts'],
                'Shazam': df.iloc[0]['in_shazam_charts']}

   fig = px.bar(x=song_dict.keys(), y=song_dict.values())
   fig.update_layout(title='Rankings of Streaming Services', xaxis_title='Platforms', yaxis_title='Charts')

   return fig

# step 1: define the app object
app = Dash(__name__)


# step 2: define the layout
app.layout = html.Div(children=[
   # elements from the top of the page
   html.Div([
      html.H1(children='How Many Playlists Were Songs in vs. Chart Rankings'),
      html.Div(children='''
      Choose Streaming Platform'''),
        dcc.Dropdown(
           id="dropdown",
           options=['apple', 'deezer', 'spotify'],
           value='apple',
           clearable=False
       ),
        dcc.Graph(id="graph1")
   ]),
   # New Div for all elements in the new 'row' of the page
   html.Div([
      html.H1(children='When Songs Were Released'),
      html.Div(children='''
      View in day or month mode? '''),

        dcc.RadioItems(
            id = 'radio',
            options=['Months', 'Days'],
            value='Months',
        ),
       html.P(html.Br()),
       html.P('Range of Dates?'),
        dcc.RangeSlider(
            id='range',
            min = 0,
            max = 11,
            step = None,
            marks = {
                0: 'Jan',
                1: 'Feb',
                2: 'Mar',
                3: 'Apr',
                4: 'May',
                5: 'Jun',
                6: 'Jul',
                7: 'Aug',
                8: 'Sep',
                9: 'Oct',
                10: 'Nov',
                11: 'Dec',
            },
            value = [0, 12]
        ),
        dcc.Graph(id="graph2")
   ]),
    html.Div([
        html.H1(children='Chart Rankings for One Song'),
        html.Div(children='''
        Enter Song Name (please format exactly how it was released)'''),
        dcc.Input(
            id='input',
            placeholder='Enter song name...',
            type='text',
            value=''
        ),
        dcc.Graph(id="graph3")
   ]),
])


# step 3: Define the callback which triggers visualization updates in response to changing the control settings

@app.callback(
    Output("graph1", "figure"),
    Output("graph2", "figure"),
    Output("graph3", "figure"),
    Input("dropdown", "value"),
    Input("radio", "value"),
    Input("range", "value"),
    Input("input", "value")
)

def dash_vis(platform, day_or_month, month_range, name):
    # df = pd.read_csv('spotify-2023.csv')
    df = pd.read_csv('test.csv')
    fig1 = rank_vis(df, platform)
    fig2 = create_hist(df, day_or_month, month_range)
    fig3 = input_song(df, name)

    return fig1, fig2, fig3


# step 4: Run the server
app.run_server(debug=True)
