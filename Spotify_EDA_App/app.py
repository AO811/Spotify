import streamlit as st
import pandas as pd
from datetime import datetime
import ast
import plotly.express as px

# -----------------------------
# Load datasets
# -----------------------------
@st.cache_data
def load_data():
    artists = pd.read_csv("../data/artists.csv")
    tracks = pd.read_csv("../data/tracks.csv")
    features = pd.read_csv("../data/SpotifyFeatures.csv")
    return artists, tracks, features

artists, tracks, features = load_data()

# -----------------------------
# Clean datasets
# -----------------------------
@st.cache_data
def clean_artists(df):
    df = df.copy()
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df['followers'] = pd.to_numeric(df['followers'], errors='coerce').fillna(0).astype(int)
    df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce').fillna(0).astype(int)
    df['genres'] = df['genres'].fillna("Unknown").str.lower()
    df['name'] = df['name'].fillna("Unknown")
    return df

@st.cache_data
def clean_tracks(df):
    df = df.copy()
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    df['name'] = df['name'].fillna("Unknown")
    return df

artists = clean_artists(artists)
tracks = clean_tracks(tracks)

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

artist_list = sorted(artists['name'].dropna().unique())
selected_artist = st.sidebar.selectbox("Artist", ["All"] + artist_list)

genre_list = sorted(artists['genres'].dropna().unique())
selected_genre = st.sidebar.selectbox("Genre", ["All"] + genre_list)

min_year = tracks['release_date'].dt.year.min()
max_year = tracks['release_date'].dt.year.max()
selected_year = st.sidebar.slider("Year Range", int(min_year), int(max_year), (int(min_year), int(max_year)))

top_n_tracks = st.sidebar.slider("Top N Tracks", 5, 50, 10)
top_n_artists = st.sidebar.slider("Top N Artists", 5, 50, 10)

# -----------------------------
# Cached filtered datasets
# -----------------------------
@st.cache_data
def get_filtered_tracks(tracks, artist, year_range):
    df = tracks.copy()
    if artist != "All":
        df = df[df['artists'] == artist]
    df = df[(df['release_date'].dt.year >= year_range[0]) & (df['release_date'].dt.year <= year_range[1])]
    return df

@st.cache_data
def get_filtered_artists(artists, artist, genre):
    df = artists.copy()
    if artist != "All":
        df = df[df['name'] == artist]
    if genre != "All":
        df = df[df['genres'] == genre]
    return df

@st.cache_data
def get_exploded_genres(df):
    df['genres_list'] = df['genres'].apply(lambda x: ast.literal_eval(x) if x.startswith("[") else [x])
    return df.explode('genres_list')

@st.cache_data
def get_correlation_heatmap(df):
    numeric_features = df.select_dtypes(include='number')
    corr = numeric_features.corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale='Viridis', aspect="auto")
    return fig

filtered_tracks = get_filtered_tracks(tracks, selected_artist, selected_year)
filtered_artists = get_filtered_artists(artists, selected_artist, selected_genre)
exploded_artists = get_exploded_genres(artists)

# -----------------------------
# Tabs for lazy loading
# -----------------------------
st.title("🎵 Spotify EDA Dashboard")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Filtered Tracks", "Filtered Artists",
    "Top Tracks & Artists", "Genres", "Popularity Trend", "Correlation Heatmap"
])

# -----------------------------
# Tab 1: Filtered Tracks
# -----------------------------
with tab1:
    st.subheader("Filtered Tracks")
    st.dataframe(filtered_tracks)

# -----------------------------
# Tab 2: Filtered Artists
# -----------------------------
with tab2:
    st.subheader("Filtered Artists")
    st.dataframe(filtered_artists)

# -----------------------------
# Tab 3: Top Tracks & Artists
# -----------------------------
with tab3:
    st.subheader(f"Top {top_n_tracks} Tracks by Popularity")
    top_tracks = filtered_tracks.sort_values('popularity', ascending=False).head(top_n_tracks)
    st.dataframe(top_tracks[['name','popularity']])
    fig = px.bar(top_tracks, x='popularity', y='name', orientation='h', text='popularity',
                 labels={'popularity':'Popularity', 'name':'Track'}, color='popularity', color_continuous_scale='Viridis')
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"Top {top_n_artists} Artists by Followers")
    top_artists = filtered_artists.sort_values('followers', ascending=False).head(top_n_artists)
    st.dataframe(top_artists[['name','followers']])
    fig = px.bar(top_artists, x='followers', y='name', orientation='h', text='followers',
                 labels={'followers':'Followers', 'name':'Artist'}, color='followers', color_continuous_scale='Magma')
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=500)
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Tab 4: Genre Distribution
# -----------------------------
with tab4:
    st.subheader("Genre Distribution (Top 15)")
    genre_counts = exploded_artists['genres_list'].value_counts().head(15)
    st.dataframe(genre_counts)
    genre_df = genre_counts.reset_index()
    genre_df.columns = ['genre', 'count']
    fig = px.bar(
        genre_df,
        x='genre',
        y='count',
        text='count',
        labels={'genre':'Genre', 'count':'Count'},
        color='count',
        color_continuous_scale='Plasma'
    )
    fig.update_layout(xaxis_tickangle=-45, height=500)
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Tab 5: Popularity Trend
# -----------------------------
with tab5:
    st.subheader("Average Popularity Trend Over Time")
    tracks_time = tracks.dropna(subset=['release_date']).set_index('release_date')
    popularity_trend = tracks_time['popularity'].resample('Y').mean()
    st.dataframe(popularity_trend)
    fig = px.line(popularity_trend.reset_index(), x='release_date', y='popularity', markers=True,
                  labels={'release_date':'Year', 'popularity':'Average Popularity'})
    fig.update_layout(xaxis=dict(tickformat='%Y'), height=500)
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Tab 6: Correlation Heatmap
# -----------------------------
with tab6:
    st.subheader("Correlation Heatmap of Numeric Features")
    fig = get_correlation_heatmap(features)
    st.plotly_chart(fig, use_container_width=True)
