# -*- coding: utf-8 -*-
from lastfm_to_spotify import Playlist


def main() -> None:
    playlist_creator = Playlist(
        # don't provide secrets if os.environ is set
        lastfm_api_key="...",
        lastfm_api_secret="...",
        spotipy_client_id="...",
        spotipy_client_secret="...",
        spotipy_redirect_uri="...",
    )
    # raises an error if playlist already exists
    # ValueError: Top Tracks May 2023 already exists:
    # id=..., use `.update_playlist` method instead.
    playlist_creator.create_playlist(
        lastfm_username="hp0404",
        playlist="Top Tracks May 2023",
        limit=1,
        period="overall",
    )

    # adds 1 track
    playlist_creator.update_playlist(
        lastfm_username="hp0404",
        playlist="Top Tracks May 2023",
        limit=1,
        period="overall",
    )

    # replaces all songs with new items
    playlist_creator.update_playlist(
        lastfm_username="hp0404",
        playlist="Top Tracks May 2023",
        limit=3,
        period="overall",
        replace_existing_tracks=True,
    )


if __name__ == "__main__":
    main()
