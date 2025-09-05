"""
Configuration settings for Spotify EDA project.
"""

# Analysis parameters
POPULARITY_THRESHOLD = 90   # min popularity for top tracks
TOP_N_TRACKS = 10           # number of top tracks to display
TOP_N_ARTISTS = 10          # number of top artists to display
TOP_N_GENRES = 15           # number of top genres to plot

# Time series analysis
POPULARITY_FREQ = "Y"       # 'Y' = yearly, 'M' = monthly
POPULARITY_FREQ_LABEL = "Yearly"

# Visualization
FIGSIZE = (12, 6)           # default figure size for bar/line plots

