import pandas as pd

# Convert artists.csv
artists = pd.read_csv("data/artists.csv")  # adjust path if needed
artists.to_parquet("data/artists.parquet", index=False)
print("artists.csv converted to artists.parquet")

# Convert tracks.csv
tracks = pd.read_csv("data/tracks.csv")
tracks.to_parquet("data/tracks.parquet", index=False)
print("tracks.csv converted to tracks.parquet")

# Convert SpotifyFeatures.csv
features = pd.read_csv("data/SpotifyFeatures.csv")
features.to_parquet("data/SpotifyFeatures.parquet", index=False)
print("SpotifyFeatures.csv converted to SpotifyFeatures.parquet")
