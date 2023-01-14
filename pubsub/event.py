import re
from abc import ABC
from typing import Any, Dict


class Event(ABC):
    data: Any
    metadata: Dict[str, str]

    def __init__(self, data: Dict[str, Any], metadata: Dict[str, str]):
        self.data = data
        self.metadata = metadata
        self.metadata["event_name"] = self.name()

    @classmethod
    def name(cls) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()


class UserRegistered(Event):
    """Simple event emitted when a new user is registered."""

    pass


class UserLoggedIn(Event):
    """Simple event emitted when a user logs in."""

    pass
