import pandas as pd

def clean_artists(artists: pd.DataFrame) -> pd.DataFrame:
    """Clean artists dataset."""
    df = artists.copy()
    
    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    
    # Handle missing values
    df['genres'] = df['genres'].fillna("Unknown")
    df['followers'] = df['followers'].fillna(0).astype(int)
    df['popularity'] = df['popularity'].fillna(0).astype(int)
    
    # Clean up genres formatting
    df['genres'] = (
        df['genres']
        .astype(str)
        .str.replace(r"[\[\]']", "", regex=True)  # remove [] and quotes
        .str.strip()
        .str.lower()
    )
    
    # Remove duplicates
    df.drop_duplicates(subset=['id'], inplace=True)
    
    return df



def clean_tracks(tracks: pd.DataFrame) -> pd.DataFrame:
    """Clean tracks dataset."""
    df = tracks.copy()
    
    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    
    # Convert release_date to datetime
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    
    # Handle missing values
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    # Remove duplicates
    df.drop_duplicates(subset=['id'], inplace=True)
    
    return df


def clean_features(features: pd.DataFrame) -> pd.DataFrame:
    """Clean Spotify features dataset."""
    df = features.copy()
    
    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    
    # Handle missing values
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    # Remove duplicates
    df.drop_duplicates(subset=['track_id'], inplace=True)
    
    return df


def clean_data(artists, tracks, features):
    """Run cleaning on all datasets."""
    artists = clean_artists(artists)
    tracks = clean_tracks(tracks)
    features = clean_features(features)
    return artists, tracks, features
