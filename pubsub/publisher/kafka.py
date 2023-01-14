import json
from typing import Dict, List, Tuple

from kafka import KafkaProducer

from pubsub.event import Event
from pubsub.publisher.protocol import PublisherProtocol


class KafkaPublisher(PublisherProtocol):
    def __init__(self, broker_address: str) -> None:
        self._producer = KafkaProducer(
            bootstrap_servers=broker_address,
            value_serializer=lambda m: json.dumps(m).encode("utf-8"),
        )

    def publish(self, event: Event, topic: str) -> None:
        self._producer.send(
            topic, value=event.data, headers=self._transform_headers(event.metadata)
        )

    @staticmethod
    def _transform_headers(headers: Dict[str, str]) -> List[Tuple[str, bytes]]:
        return [(key, value.encode("utf-8")) for key, value in headers.items()]
