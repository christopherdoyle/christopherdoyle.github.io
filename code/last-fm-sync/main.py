import dataclasses
import os
import sys
from typing import Literal

import requests
import yaml


class LastFmApi:
    base_uri = "https://ws.audioscrobbler.com/2.0"

    def __init__(self, api_key: str):
        self._api_key = api_key

    def do_api_call(self, uri: str, params: dict, format_: Literal["json", "xml"] = "json") -> requests.Response:
        params = dict(params)
        if "api_key" not in params:
            params.update(dict(api_key=self._api_key))
        if "format" not in params:
            params.update(dict(format=format_))
        return requests.get(uri, params, timeout=3)

    def get_top_tracks(self, username: str, period: Literal["overall", "7day", "1month", "3month", "6month", "12month"], limit: int = 50):
        return self.do_api_call(
            self.base_uri,
            dict( method="user.gettoptracks", user=username, period=period, limit=limit)
        )


def get_top_track_this_month():
    api_key = os.environ["LAST_FM_API_KEY"]
    last_fm_api = LastFmApi(api_key)
    result = last_fm_api.get_top_tracks(
        username=os.environ["LAST_FM_USER"],
        period="1month",
        limit=1,
    )
    if result.status_code == 200:
        top_track = result.json()["toptracks"]["track"][0]
        track_name = top_track["name"]
        artist = top_track["artist"]["name"]
        playcount = int(top_track["playcount"])
        return track_name, artist, playcount
    else:
        raise ValueError("Failed to lookup top track")


def update_config(track, artist, playcount):
    config_filepath = "../../_config.yml"

    with open(config_filepath, "r", encoding="utf8") as fh:
        data = yaml.safe_load(fh)

    if "top_track" not in data:
        data["top_track"] = {}
    data["top_track"]["name"] = track
    data["top_track"]["artist"] = artist
    data["top_track"]["playcount"] = playcount

    with open(config_filepath, "w", encoding="utf8") as fh:
        yaml.safe_dump(data, fh, default_flow_style=False)


def main():
    track, artist, playcount = get_top_track_this_month(config)
    update_config(track, artist, playcount)


if __name__ == "__main__":
    main()
