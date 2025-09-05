import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_correlation_heatmap(
    df: pd.DataFrame,
    title: str = "Feature Correlation Heatmap",
    save_path: str = None
):
    """
    Plot a correlation heatmap of numeric features in a DataFrame.
    If save_path is provided, save the figure instead of showing it.
    """
    numeric_df = df.select_dtypes(include='number')
    if numeric_df.empty or numeric_df.shape[1] < 2:
        return

    plt.figure(figsize=(12, 8))
    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        cmap='viridis',
        fmt='.2f',
        linewidths=0.5,
        linecolor='black'
    )
    plt.title(title)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.close()
    else:
        plt.show()


def plot_genre_distribution(
    genre_counts: pd.Series,
    top_n: int = 15,
    save_path: str = None
):
    """
    Plot a bar chart of the most common genres.
    """
    if genre_counts is None or genre_counts.empty:
        return

    plt.figure(figsize=(12, 6))
    genre_counts.head(top_n).plot(kind='bar', edgecolor='black')
    plt.title(f"Top {top_n} Genres")
    plt.xlabel("Genre")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.close()
    else:
        plt.show()


def plot_popularity_trend(
    popularity_series: pd.Series,
    freq_label: str = "Yearly",
    save_path: str = None
):
    """
    Plot the average popularity trend over time.
    """
    if popularity_series is None or popularity_series.empty:
        return

    plt.figure(figsize=(12, 6))
    popularity_series.plot(marker='o')
    plt.title(f"Average Track Popularity Over Time ({freq_label})")
    plt.xlabel("Time")
    plt.ylabel("Average Popularity")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.close()
    else:
        plt.show()


def plot_top_entities(
    df: pd.DataFrame,
    column: str,
    value_col: str,
    top_n: int = 10,
    title: str = "Top Entities",
    save_path: str = None
):
    """
    Generic bar plot for top entities (artists, tracks, etc.)
    df: DataFrame
    column: name column (e.g., 'name' for tracks, 'name' for artists)
    value_col: numeric column to rank by (e.g., 'followers', 'popularity')
    """
    if df is None or df.empty:
        return

    if column not in df.columns or value_col not in df.columns:
        return

    top_entities = df[[column, value_col]].sort_values(value_col, ascending=False).head(top_n)
    if top_entities.empty:
        return

    plt.figure(figsize=(12, 6))
    sns.barplot(x=value_col, y=column, data=top_entities)
    plt.title(title)
    plt.xlabel(value_col.capitalize())
    plt.ylabel(column.capitalize())
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.close()
    else:
        plt.show()
