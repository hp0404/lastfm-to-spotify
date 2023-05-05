# -*- coding: utf-8 -*-
import argparse
from . import PlaylistCreator


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a Spotify playlist from top LastFM tracks."
    )
    parser.add_argument(
        "-u",
        "--username",
        required=True,
        help="The LastFM username to fetch top tracks.",
    )
    parser.add_argument(
        "-n",
        "--playlist",
        required=True,
        help="The name of the Spotify playlist to create or update.",
    )
    parser.add_argument(
        "-p",
        "--period",
        default="3month",
        choices=["overall", "7day", "1month", "3month", "6month", "12month"],
        help="The time period to consider for top tracks.",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=30,
        help="The number of top tracks to include in the playlist.",
    )
    args = parser.parse_args()

    playlist_creator = PlaylistCreator(
        lastfm_username=args.username,
        playlist_name=args.playlist,
        period=args.period,
        limit=args.limit
    )
    playlist_creator.create_or_update_playlist()


if __name__ == "__main__":
    main()
