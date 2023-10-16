import matplotlib.pyplot as plt
import pandas as pd

def input_song(name):

    df = pd.read_csv('/Users/mel/Desktop/DS3500/spotify-2023.csv')


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
        plt.bar(platforms, charts)
        plt.title('Rankings of Streaming Services')
        plt.xlabel('Platforms')
        plt.ylabel('Charts')

        plt.tight_layout()
        plt.show()


input_song("Lucid Dreams")