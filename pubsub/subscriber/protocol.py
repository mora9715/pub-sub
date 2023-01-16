from typing import Callable, Dict, List, Protocol, Type

from pubsub.event import Event


class SubscribeProtocol(Protocol):
    topic: str
    subscriptions: Dict[Type[Event], List[Callable[[Event], None]]]

    def subscribe(self, event_cls: Type[Event], handler: Callable) -> None:
        """Subscribe to an event, specifying a callable responsible for handling the event."""
        pass

    def unsubscribe(self, event_cls: Type[Event], handler: Callable) -> None:
        """Unsubscribe from an event."""
        pass

    def listen(self) -> None:
        """Listen for incoming events, delegating handling to corresponding handlers if needed."""
        pass
