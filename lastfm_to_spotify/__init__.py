# -*- coding: utf-8 -*-
import os
import typing

import pylast
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class PlaylistCreator:
    def __init__(
        self,
        lastfm_username: str,
        playlist_name: str,
        period: str = "3month",
        limit: int = 30,
        lastfm_api_key: typing.Optional[str] = None,
        lastfm_api_secret: typing.Optional[str] = None,
        spotipy_client_id: typing.Optional[str] = None,
        spotipy_client_secret: typing.Optional[str] = None,
        spotipy_redirect_uri: typing.Optional[str] = None,
    ):
        self.period = period
        self.limit = limit
        self.lastfm_username = lastfm_username
        self.playlist_name = playlist_name
        self.user_id: typing.Optional[str] = None
        self.network = pylast.LastFMNetwork(
            api_key=lastfm_api_key or os.environ["LASTFM_API_KEY"],
            api_secret=lastfm_api_secret or os.environ["LASTFM_API_SECRET"],
        )
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=spotipy_client_id or os.environ["SPOTIPY_CLIENT_ID"],
                client_secret=spotipy_client_secret or os.environ["SPOTIPY_CLIENT_SECRET"],
                redirect_uri=spotipy_redirect_uri or os.environ["SPOTIPY_REDIRECT_URI"],
                scope="playlist-modify-public",
            )
        )

    def get_lastfm_tracks(self, user: pylast.User) -> typing.List[pylast.TopItem]:
        return user.get_top_tracks(period=self.period, limit=self.limit)

    def get_spotify_playlist(self) -> str:
        playlist_id: typing.Optional[str] = None
        for name in self.sp.user_playlists(self.user_id)["items"]:
            if name["name"] == self.playlist_name:
                playlist_id = name["id"]
                break
        # if doesn't exist, create new playlist
        if playlist_id is None:
            new_playlist = self.sp.user_playlist_create(
                self.user_id, name=self.playlist_name
            )
            playlist_id = new_playlist["id"]
        return playlist_id

    def get_track_uris(self, tracks: typing.List[pylast.TopItem]) -> typing.List[str]:
        track_uris = []
        for track in tracks:
            search_query = f"{track.item.artist.name} {track.item.title}"
            results = self.sp.search(search_query, type="track")
            if results["tracks"]["items"]:
                track_uris.append(results["tracks"]["items"][0]["uri"])
        return track_uris

    def create_or_update_playlist(self) -> None:
        user = pylast.User(self.lastfm_username, network=self.network)
        tracks = self.get_lastfm_tracks(user)

        self.user_id = self.sp.me()["id"]
        playlist_id = self.get_spotify_playlist()
        track_uris = self.get_track_uris(tracks)
        self.sp.playlist_add_items(playlist_id, items=track_uris)
