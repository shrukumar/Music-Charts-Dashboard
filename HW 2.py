from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import random as rnd
from collections import Counter
import pandas as pd


# https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023

def main():

    # step 1: define the app object
    app = Dash(__name__)

