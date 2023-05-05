# LastFM to Spotify Playlist Creator

This Python library and CLI tool allows you to create or update a Spotify playlist with your top tracks from LastFM. 
You can specify the time period and the number of tracks to include in the playlist.

## Installation
To use or contribute to this repository, first checkout the code. Then create a new virtual environment:

```terminal
$ git clone https://github.com/hp0404/lastfm-to-spotify.git
$ cd lastfm-to-spotify
$ python3 -m venv env
$ . env/bin/activate
$ pip install .
```

Alternatively, instead of pip you could use poetry:
```terminal
$ poetry install
```

## Usage

Here's a short example of how to use Playlist Creator:

```python
from lastfm_to_spotify import PlaylistCreator

username = "myusername"
playlist_name = "My Top Tracks"

playlist_creator = PlaylistCreator(lastfm_username, playlist_name)
playlist_creator.create_or_update_playlist()
```

This code will create a new Spotify playlist called "My Top Tracks" (if it doesn't already exist) and add the user's top tracks from the last 3 months.

Note that the example above assumes you have environment variables set up, but you can also provide them, e.g.

```python
...
playlist_creator = PlaylistCreator(
    lastfm_username,
    playlist_name,
    lastfm_api_key="...",
    lastfm_api_secret="...",
    spotipy_client_id="...",
    spotipy_client_secret="...",
)
...
```

You can also use command-line interface, see `--help` for more:
```terminal
$ lastfm-to-spotify --username hp0404 --playlist "Top Tracks May 2023" --period "1month" --limit 7
```

or

```terminal
$ poetry run lastfm-to-spotify --username hp0404 --playlist "Top Tracks May 2023" --period "1month" --limit 7
```

## Dependencies
- `pylast` (for Last.fm API access)
- `spotipy` (for Spotify API access)

## Configuration
In order to use the Spotify API, you need to have a Spotify account and create a Spotify app to obtain a client ID and client secret. 

You also need to set up environment variables for the Last.fm API key and secret.
