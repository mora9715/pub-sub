from typing import Protocol

from pubsub.event import Event


class PublisherProtocol(Protocol):
    def publish(self, event: Event, topic: str) -> None:
        pass
