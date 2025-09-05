import logging
import os
import src.config as cfg

from src.loader import load_datasets
from src.cleaner import clean_data
from src.analyzer import (
    get_top_popular_tracks,
    top_artists_by_followers,
    genre_distribution,
    popularity_trend
)
from src.visualizer import (
    plot_correlation_heatmap,
    plot_genre_distribution,
    plot_popularity_trend,
    plot_top_entities
)

# === Setup results directory ===
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# === Configure logging ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(RESULTS_DIR, "run.log"), mode="w"),
        logging.StreamHandler()
    ]
)


def save_results(results):
    """Save analysis results as CSV and JSON in results/ folder."""
    logging.info("Saving analysis results...")

    results["top_tracks"].to_csv(os.path.join(RESULTS_DIR, "top_tracks.csv"), index=False)
    results["top_tracks"].to_json(os.path.join(RESULTS_DIR, "top_tracks.json"), orient="records", indent=2)

    results["top_artists"].to_csv(os.path.join(RESULTS_DIR, "top_artists.csv"), index=False)
    results["top_artists"].to_json(os.path.join(RESULTS_DIR, "top_artists.json"), orient="records", indent=2)

    results["genres"].to_csv(os.path.join(RESULTS_DIR, "genre_distribution.csv"))
    results["popularity_trend"].to_csv(os.path.join(RESULTS_DIR, "popularity_trend.csv"))


def run_analysis(artists, tracks, features):
    """Run analysis and return results as dict."""
    results = {}

    logging.info("Analyzing top popular tracks...")
    results["top_tracks"] = get_top_popular_tracks(
        tracks,
        threshold=cfg.POPULARITY_THRESHOLD,
        top_n=cfg.TOP_N_TRACKS
    )

    logging.info("Analyzing top artists by followers...")
    results["top_artists"] = top_artists_by_followers(
        artists,
        top_n=cfg.TOP_N_ARTISTS
    )

    logging.info("Analyzing genre distribution...")
    results["genres"] = genre_distribution(artists)

    logging.info("Analyzing popularity trend...")
    results["popularity_trend"] = popularity_trend(
        tracks,
        freq=cfg.POPULARITY_FREQ
    )

    return results


def display_results(results):
    """Pretty print summary analysis results."""
    print("\n=== Top Popular Tracks ===")
    print(results["top_tracks"][["name", "popularity"]])

    print("\n=== Top Artists by Followers ===")
    print(results["top_artists"][["name", "followers"]])

    print(f"\n=== Genre Distribution (Top {cfg.TOP_N_GENRES}) ===")
    print(results["genres"].head(cfg.TOP_N_GENRES))

    print(f"\n=== Popularity Trend ({cfg.POPULARITY_FREQ_LABEL}) ===")
    print(results["popularity_trend"].tail())


def generate_visuals(results, features):
    """Generate plots from analysis results and save them to results/ folder."""
    logging.info("Generating visualizations...")

    plot_correlation_heatmap(
        features,
        save_path=os.path.join(RESULTS_DIR, "correlation_heatmap.png")
    )

    plot_genre_distribution(
        results["genres"],
        top_n=cfg.TOP_N_GENRES,
        save_path=os.path.join(RESULTS_DIR, "genre_distribution.png")
    )

    plot_popularity_trend(
        results["popularity_trend"],
        freq_label=cfg.POPULARITY_FREQ_LABEL,
        save_path=os.path.join(RESULTS_DIR, "popularity_trend.png")
    )

    plot_top_entities(
        results["top_artists"],
        column="name",
        value_col="followers",
        top_n=cfg.TOP_N_ARTISTS,
        title=f"Top {cfg.TOP_N_ARTISTS} Artists by Followers",
        save_path=os.path.join(RESULTS_DIR, "top_artists.png")
    )

    plot_top_entities(
        results["top_tracks"],
        column="name",
        value_col="popularity",
        top_n=cfg.TOP_N_TRACKS,
        title=f"Top {cfg.TOP_N_TRACKS} Tracks by Popularity",
        save_path=os.path.join(RESULTS_DIR, "top_tracks.png")
    )


def main():
    logging.info("Loading datasets...")
    artists, tracks, features = load_datasets()

    logging.info("Cleaning datasets...")
    artists, tracks, features = clean_data(artists, tracks, features)

    results = run_analysis(artists, tracks, features)

    display_results(results)

    save_results(results)

    generate_visuals(results, features)

    logging.info("Analysis complete.")


if __name__ == "__main__":
    main()
