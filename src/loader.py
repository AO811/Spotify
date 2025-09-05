import os
import pandas as pd

def load_datasets():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")
    artist = pd.read_csv(os.path.join(data_dir, "artists.csv"))
    tracks = pd.read_csv(os.path.join(data_dir, "tracks.csv"))
    spotify_features = pd.read_csv(os.path.join(data_dir, "SpotifyFeatures.csv"))
    return artist, tracks, spotify_features
