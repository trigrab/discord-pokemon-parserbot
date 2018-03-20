# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timezone


class Raid:
    """Class for representing spawns of pokemon."""
    _despawn_time: datetime = None
    pokemon_number: int = None
    latitude: float = None
    longitude: float = None
    lvl: int = None
    attacks: str = None
    arena: str = None

    @property
    def despawn_time(self):
        return self._despawn_time.isoformat()

    @despawn_time.setter
    def despawn_time(self, despawn_time):
        self._despawn_time = despawn_time
        self._despawn_time.replace(tzinfo=timezone.utc).astimezone(tz=None)

    def as_dict(self):
        return [(a, getattr(self, a)) for a in dir(self) if
                not callable(getattr(self, a)) and a[0] != '_']
