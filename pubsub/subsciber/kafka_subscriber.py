import json
from typing import Any, Callable, Dict, List, Tuple, Type

from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord

from pubsub.event import Event

from .protocol import SubscribeProtocol


class KafkaSubscriber(SubscribeProtocol):
    event_header_name = "event_name"

    def __init__(self, topic: str, subscriber_name: str, broker_address: str):
        self.topic = topic
        self.subscriptions = {}
        self._consumer = KafkaConsumer(
            self.topic,
            group_id=subscriber_name,
            bootstrap_servers=[broker_address],
            value_deserializer=self._message_data_deserializer,
        )

    def subscribe(self, event_cls: Type[Event], handler: Callable) -> None:
        if event_cls not in self.subscriptions:
            self.subscriptions[event_cls] = handler

    def unsubscribe(self, event_cls: Type[Event]) -> None:
        if event_cls in self.subscriptions:
            self.subscriptions.pop(event_cls)

    def listen(self) -> None:
        message: ConsumerRecord
        for message in self._consumer:
            self._process_single_message(message)

    def _process_single_message(self, message: ConsumerRecord) -> None:
        headers = self._transform_headers(message.headers)
        if self.event_header_name not in headers:
            return

        event_name = headers.pop(self.event_header_name)
        for event_cls, handler in self.subscriptions.items():
            if event_cls.name() == event_name:
                # TODO: delegate to process pool executor
                handler(event_cls(data=message.value, metadata=headers))
                return

    @staticmethod
    def _transform_headers(headers: List[Tuple[str, bytes]]) -> Dict[str, str]:
        return {key: value.decode("utf-8") for key, value in headers}

    @staticmethod
    def _message_data_deserializer(value: bytes) -> Any:
        return json.loads(value.decode("utf-8"))
