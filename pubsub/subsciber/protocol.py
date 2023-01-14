from typing import Callable, Dict, Protocol, Type

from pubsub.event import Event


class SubscribeProtocol(Protocol):
    topic: str
    subscriptions: Dict[Type[Event], Callable[[Event], None]]

    def subscribe(self, event_cls: Type[Event], handler: Callable) -> None:
        pass

    def unsubscribe(self, event_cls: Type[Event]) -> None:
        pass

    def listen(self) -> None:
        pass
