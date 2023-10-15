import plotly.express as px
import pandas as pd
from datetime import datetime
from dash import Dash, dcc, html, Input, Output

# step 1: define the app object
app = Dash(__name__)

# step 2: define the layout
app.layout = html.Div([
    html.H4("Song Release Dates"),
    html.P('View by months or days?'),
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
    dcc.Graph(id="hist")
])

# step 3: Define the callback which triggers visualization updates
#         in response to changing the control settings

@app.callback(
    Output("hist", "figure"),
    Input("radio", "value"),
    Input("range", "value")
)
def create_hist(day_or_month, month_range):
    """
    creates histogram with data about song release dates, can be viewed in months or days and customizable range
    Args:
        day_or_month (str): string indicating to create hist with month or day info
        month_range (ls): list with range of months to limit graph
    Returns:
         fig (plotly.histogram): histogram with song release data
    """
    csv = 'spotify-2023.csv'

    # creating df and dropping nan
    df_song = pd.read_csv(csv)
    df = df_song.dropna()

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


# step 4: Run the server
app.run_server(debug=True)
