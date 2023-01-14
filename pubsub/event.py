import re
from abc import ABC
from typing import Any, Dict


class Event(ABC):
    data: Any
    metadata: Dict[str, str]

    def __init__(self, data: Dict[str, Any], metadata: Dict[str, str]):
        self.data = data
        self.metadata = metadata

    @classmethod
    def name(cls) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()


class UserRegistered(Event):
    pass


class UserLoggedIn(Event):
    pass
