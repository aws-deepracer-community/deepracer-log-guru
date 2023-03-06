#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#
from prototype_ui.hot_rod_super_speedway_cw_track import HotRodSuperSpeedwayClockwiseTrack
from prototype_ui.reinvent_2018_track_v4 import Reinvent2018Track
from prototype_ui.track_v4 import Track


def get_all_tracks() -> dict[str: Track]:
    tracks = {}

    for t in [Reinvent2018Track(), HotRodSuperSpeedwayClockwiseTrack()
              ]:
        t.prepare(tracks)

    return tracks
