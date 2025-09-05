import pandas as pd
from typing import Optional
import ast


def get_top_popular_tracks(tracks: pd.DataFrame, threshold: Optional[int] = 90, top_n: int = 10) -> pd.DataFrame:
    """
    Return the top tracks with popularity above a threshold.
    If threshold is None, return the top `top_n` tracks by popularity.
    """
    if 'popularity' not in tracks.columns:
        return tracks.head(0)

    df = tracks.copy()
    df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce').fillna(0).astype(int)

    if threshold is not None:
        filtered = df[df['popularity'] > int(threshold)]
    else:
        filtered = df

    return filtered.sort_values('popularity', ascending=False).head(top_n)


def set_release_date_index(tracks: pd.DataFrame) -> pd.DataFrame:
    """
    Set 'release_date' as the DataFrame index. Ensures the column is datetime.
    """
    df = tracks.copy()
    if "release_date" in df.columns:
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        df = df.set_index('release_date')
    return df


def top_artists_by_followers(artists: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Return top artists ranked by followers (handles non-numeric followers).
    """
    if 'followers' not in artists.columns:
        return artists.head(0)

    df = artists.copy()
    df['followers'] = pd.to_numeric(df['followers'], errors='coerce').fillna(0).astype(int)
    return df.sort_values('followers', ascending=False).head(top_n)


def genre_distribution(artists: pd.DataFrame) -> pd.Series:
    """
    Compute the distribution of genres across all artists.
    Handles cases where genres are lists, stringified lists, or comma-separated strings.
    """
    if "genres" not in artists.columns:
        return pd.Series(dtype=int)

    all_genres = []

    for val in artists["genres"].dropna():
        # If already a list
        if isinstance(val, list):
            all_genres.extend(val)

        # If it's a string, try parsing
        elif isinstance(val, str):
            try:
                parsed = ast.literal_eval(val)  # e.g. "['pop','rock']"
                if isinstance(parsed, list):
                    all_genres.extend(parsed)
                else:
                    # fallback: split by comma
                    all_genres.extend([g.strip() for g in val.split(",")])
            except (ValueError, SyntaxError):
                # fallback if parsing fails
                all_genres.extend([g.strip() for g in val.split(",")])

    return pd.Series(all_genres).value_counts()

def popularity_trend(tracks: pd.DataFrame, freq: str = "YE") -> pd.Series:
    """
    Return average track popularity over time.
    Default freq is 'YE' (year end). If user passes 'Y', it will be mapped to 'YE'
    for backward compatibility with older code that used 'Y'.
    """
    if "release_date" not in tracks.columns:
        return pd.Series(dtype=float)

    df = tracks.copy()
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df = df.dropna(subset=['release_date'])

    # Ensure popularity is numeric (NaNs are allowed; resample mean will skip them)
    if 'popularity' in df.columns:
        df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce')

    # Backwards compatibility: map deprecated 'Y' to 'YE'
    freq_upper = str(freq).upper()
    if freq_upper == 'Y':
        freq = 'YE'

    df = df.set_index('release_date')
    return df['popularity'].resample(freq).mean()
