from enum import Enum, auto

class XonixEvent(Enum):
    START_GAME = auto()
    RESUME_GAME = auto()
    RETRY_LEVEL = auto()
    NEXT_LEVEL = auto()
    SHOW_MENU = auto()
    EXIT_GAME = auto()
    TOGGLE_FULLSCREEN = auto()

class XonixEventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type, handler):
        self._subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event_type, **data):
        for handler in self._subscribers.get(event_type, []):
            handler(**data)
