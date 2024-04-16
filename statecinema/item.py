from transitions import Machine
from dataclasses import dataclass
from datetime import datetime as dt
import logging

from statecinema.exceptions import MediaStateException

# Define states and their transitions in state_machine.py for simplicity
from .states import setup_state_machine, States

@dataclass
class ItemId:
    value: str
    parent_id: 'ItemId' = None

    def __repr__(self):
        return f"{self.parent_id}/{self.value}" if self.parent_id else str(self.value)

class MediaItem:
    def __init__(self, title, imdb_id=None, is_anime=False, **kwargs):
        self.title = title
        self.imdb_id = imdb_id
        self.is_anime = is_anime
        self.parsed_data = kwargs.get('parsed_data')
        self.symlinked = False
        self.file = kwargs.get('file')
        self.folder = kwargs.get('folder')
        self.item_id = ItemId(value=imdb_id)
        self.state = States.UNKNOWN
        self.state_machine = setup_state_machine(self)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.title}, State={self.state.name})"

class Movie(MediaItem):
    def __init__(self, title, imdb_id=None, **kwargs):
        super().__init__(title, imdb_id=imdb_id, **kwargs)

class Show(MediaItem):
    def __init__(self, title, imdb_id=None, **kwargs):
        super().__init__(title, imdb_id=imdb_id, **kwargs)
        self.seasons = []

    def add_season(self, season):
        self.seasons.append(season)
        season.item_id.parent_id = self.item_id

class Season(MediaItem):
    def __init__(self, title, imdb_id=None, number=None, **kwargs):
        super().__init__(title, imdb_id=imdb_id, **kwargs)
        self.number = number
        self.episodes = []

    def add_episode(self, episode):
        self.episodes.append(episode)
        episode.item_id.parent_id = self.item_id

class Episode(MediaItem):
    def __init__(self, title, imdb_id=None, number=None, **kwargs):
        super().__init__(title, imdb_id=imdb_id, **kwargs)
        self.number = number

    def __repr__(self):
        return f"{self.__class__.__name__}({self.title}, Season={self.item_id.parent_id}, State={self.state.name})"
    
    def __str__(self):
        return f"{self.title} - S{self.item_id.parent_id.value}E{self.number}"
