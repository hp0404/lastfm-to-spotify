# -*- coding: utf-8 -*-
import typer
from . import Playlist

app = typer.Typer()


@app.command()
def create(
    username: str = typer.Option(
        ..., "-u", "--username", help="The LastFM username to fetch top tracks."
    ),
    playlist: str = typer.Option(
        ..., "-n", "--playlist", help="The name of the Spotify playlist to create."
    ),
    period: str = typer.Option(
        "3month",
        "-p",
        "--period",
        help="The time period to consider for top tracks.",
        show_choices=True,
        case_sensitive=False,
    ),
    limit: int = typer.Option(
        30, "-l", "--limit", help="The number of top tracks to include in the playlist."
    ),
):
    """Create a Spotify playlist from top LastFM tracks"""
    playlist_wrapper = Playlist()
    playlist_wrapper.create_playlist(
        lastfm_username=username, playlist=playlist, period=period, limit=limit
    )


@app.command()
def update(
    username: str = typer.Option(
        ..., "-u", "--username", help="The LastFM username to fetch top tracks."
    ),
    playlist: str = typer.Option(
        ..., "-n", "--playlist", help="The name of the Spotify playlist to update."
    ),
    period: str = typer.Option(
        "3month",
        "-p",
        "--period",
        help="The time period to consider for top tracks.",
        show_choices=True,
        case_sensitive=False,
    ),
    limit: int = typer.Option(
        30, "-l", "--limit", help="The number of top tracks to include in the playlist."
    ),
    replace: bool = typer.Option(
        False,
        "--replace",
        help="Replace existing tracks in the playlist instead of adding to them.",
    ),
):
    """Update a Spotify playlist from top LastFM tracks"""
    playlist_wrapper = Playlist()
    playlist_wrapper.update_playlist(
        lastfm_username=username,
        playlist=playlist,
        period=period,
        limit=limit,
        replace_existing_tracks=replace,
    )


def main():
    app()


if __name__ == "__main__":
    main()
