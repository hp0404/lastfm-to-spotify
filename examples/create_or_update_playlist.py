from lastfm_to_spotify import PlaylistCreator


def main() -> None:
    playlist_creator = PlaylistCreator(
        lastfm_username="hp0404", 
        playlist_name="HP - Past Sounds - test",
        period="3month",
        limit=15,
        # don't provide secrets if os.environ is set
        lastfm_api_key="...",
        lastfm_api_secret="...",
        spotipy_client_id="...",
        spotipy_client_secret="..."
    )
    playlist_creator.create_or_update_playlist()


if __name__ == "__main__":
    main()
