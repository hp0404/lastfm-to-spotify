# -*- coding: utf-8 -*-
import os
import typing

import pylast
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class Playlist:
    def __init__(
        self,
        lastfm_api_key: typing.Optional[str] = None,
        lastfm_api_secret: typing.Optional[str] = None,
        spotipy_client_id: typing.Optional[str] = None,
        spotipy_client_secret: typing.Optional[str] = None,
        spotipy_redirect_uri: typing.Optional[str] = None,
    ):
        self.lastfm_api_key = lastfm_api_key or os.environ["LASTFM_API_KEY"]
        self.lastfm_api_secret = lastfm_api_secret or os.environ["LASTFM_API_SECRET"]
        self.spotipy_client_id = spotipy_client_id or os.environ["SPOTIPY_CLIENT_ID"]
        self.spotipy_client_secret = (
            spotipy_client_secret or os.environ["SPOTIPY_CLIENT_SECRET"]
        )
        self.spotipy_redirect_uri = (
            spotipy_redirect_uri or os.environ["SPOTIPY_REDIRECT_URI"]
        )
        self.network = pylast.LastFMNetwork(
            api_key=self.lastfm_api_key, api_secret=self.lastfm_api_secret
        )
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.spotipy_client_id,
                client_secret=self.spotipy_client_secret,
                redirect_uri=self.spotipy_redirect_uri,
                scope="playlist-modify-public",
            )
        )
        self.user_id: str = self.sp.me()["id"]

    def get_lastfm_tracks(
        self, lastfm_username: str, period: str = "3month", limit: int = 30
    ) -> typing.List[pylast.TopItem]:
        user = pylast.User(lastfm_username, network=self.network)
        return user.get_top_tracks(period=period, limit=limit)

    def _get_spotify_playlist_id(self, playlist_name: str) -> typing.Optional[str]:
        playlists = self.sp.user_playlists(self.user_id)["items"]
        for playlist in playlists:
            if playlist["name"] == playlist_name:
                return playlist["id"]
        return None

    def _create_spotify_playlist(self, playlist_name: str) -> str:
        new_playlist = self.sp.user_playlist_create(self.user_id, name=playlist_name)
        return new_playlist["id"]

    def _get_spotify_uris(
        self, tracks: typing.List[pylast.TopItem]
    ) -> typing.List[str]:
        track_uris = []
        for track in tracks:
            search_query = f"{track.item.artist.name} {track.item.title}"
            results = self.sp.search(search_query, type="track")
            if results["tracks"]["items"]:
                track_uris.append(results["tracks"]["items"][0]["uri"])
        return track_uris

    def create_playlist(
        self,
        lastfm_username: str,
        playlist: str,
        period: str = "3month",
        limit: int = 30,
    ) -> None:
        playlist_id = self._get_spotify_playlist_id(playlist_name=playlist)
        if playlist_id is not None:
            raise ValueError(
                f"{playlist} already exists: id={playlist_id}, "
                "use `.update_playlist` method instead."
            )
        playlist_id = self._create_spotify_playlist(playlist_name=playlist)
        tracks = self.get_lastfm_tracks(
            lastfm_username=lastfm_username, period=period, limit=limit
        )
        spotify_uris = self._get_spotify_uris(tracks=tracks)
        self.sp.playlist_add_items(playlist_id, items=spotify_uris)

    def update_playlist(
        self,
        lastfm_username: str,
        playlist: str,
        period: str = "3month",
        limit: int = 30,
        replace_existing_tracks: bool = False,
    ) -> None:
        playlist_id = self._get_spotify_playlist_id(playlist_name=playlist)
        if playlist_id is None:
            playlist_id = self._create_spotify_playlist(playlist_name=playlist)
        tracks = self.get_lastfm_tracks(
            lastfm_username=lastfm_username, period=period, limit=limit
        )
        spotify_uris = self._get_spotify_uris(tracks=tracks)
        method = (
            self.sp.playlist_replace_items
            if replace_existing_tracks
            else self.sp.playlist_add_items
        )
        method(playlist_id, items=spotify_uris)
