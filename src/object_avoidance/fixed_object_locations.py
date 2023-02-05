from enum import Enum


class Lane(Enum):
    INSIDE = 1
    OUTSIDE = -1


class FixedObjectLocation:
    def __init__(self, percent: float, lane: Lane):
        assert 0.0 <= percent <= 1.0
        self.percent = percent
        self.lane = lane


class FixedObjectLocations:
    def __init__(self):
        self._locations: list[FixedObjectLocation] = []

    def add(self, location: FixedObjectLocation):
        self._locations.append(location)

    def has_locations(self) -> bool:
        return len(self._locations) > 0

    def get_meta_json_list(self):
        objects_json = []
        for location in self._locations:
            objects_json.append({"percent": location.percent, "lane": location.lane.name})
        return objects_json

    def set_from_meta_json_list(self):
        pass    # TODO
