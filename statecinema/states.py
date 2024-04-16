from transitions import Machine
from enum import Enum


class States(Enum):
    UNKNOWN = 'Unknown'
    REQUESTED = 'Requested'
    INDEXED = 'Indexed'
    SCRAPED = 'Scraped'
    DOWNLOADED = 'Downloaded'
    SYMLINKED = 'Symlinked'
    COMPLETED = 'Completed'
    PARTIALLY_COMPLETED = 'PartiallyCompleted'
    FAILED = 'Failed'


def setup_states(model):
    states = [state.value for state in States]
    transitions = [
        {'trigger': 'request', 'source': States.UNKNOWN.value, 'dest': States.REQUESTED.value},
        {'trigger': 'index', 'source': States.REQUESTED.value, 'dest': States.INDEXED.value},
        {'trigger': 'scrape', 'source': States.INDEXED.value, 'dest': States.SCRAPED.value},
        {'trigger': 'download', 'source': States.SCRAPED.value, 'dest': States.DOWNLOADED.value},
        {'trigger': 'symlink', 'source': States.DOWNLOADED.value, 'dest': States.SYMLINKED.value},
        {'trigger': 'complete', 'source': States.SYMLINKED.value, 'dest': States.COMPLETED.value},
        {'trigger': 'fail', 'source': [States.UNKNOWN.value, States.REQUESTED.value, States.INDEXED.value, States.SCRAPED.value, States.DOWNLOADED.value, States.SYMLINKED.value], 'dest': States.FAILED.value},
        {'trigger': 'partial_complete', 'source': [States.SYMLINKED.value, States.COMPLETED.value], 'dest': States.PARTIALLY_COMPLETED.value},
    ]

    machine = Machine(model=model, states=states, initial=States.UNKNOWN.value, transitions=transitions)
    return machine
