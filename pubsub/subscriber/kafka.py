import json
from typing import Callable, Dict, List, Tuple, Type

from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
from loguru import logger

from pubsub.event import Event
from pubsub.subscriber.protocol import SubscribeProtocol


class KafkaSubscriber(SubscribeProtocol):
    def __init__(self, topic: str, subscriber_name: str, broker_address: str) -> None:
        self.topic = topic
        self.subscriptions = {}
        self._consumer = KafkaConsumer(
            self.topic,
            group_id=subscriber_name,
            bootstrap_servers=[broker_address],
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )

    def subscribe(self, event_cls: Type[Event], handler: Callable) -> None:
        if event_cls not in self.subscriptions:
            self.subscriptions[event_cls] = handler
            logger.info(f"Subscribed to an event {event_cls.name()}")

    def unsubscribe(self, event_cls: Type[Event]) -> None:
        if event_cls in self.subscriptions:
            self.subscriptions.pop(event_cls)
            logger.info(f"Unsubscribed from an event {event_cls.name()}")

    def listen(self) -> None:
        message: ConsumerRecord
        for message in self._consumer:
            self._process_single_message(message)

    def _process_single_message(self, message: ConsumerRecord) -> None:
        headers = self._transform_headers(message.headers)
        if "event_name" not in headers:
            return

        event_name = headers.pop("event_name")
        for event_cls, handler in self.subscriptions.items():
            if event_cls.name() == event_name:
                # TODO: delegate to process pool executor
                logger.info(
                    f"Received an event {event_cls.name()}:\ndata:{message.value}\nmetadata:{headers}"
                )
                handler(event_cls(data=message.value, metadata=headers))
                return

    @staticmethod
    def _transform_headers(headers: List[Tuple[str, bytes]]) -> Dict[str, str]:
        return {key: value.decode("utf-8") for key, value in headers}
