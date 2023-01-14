import json
import os
from time import sleep

from kafka import KafkaProducer

from bootstrap import bootstrap


def main() -> None:
    producer = KafkaProducer(
        bootstrap_servers=os.environ.get("BROKER_ADDRESS", "localhost:9092"),
        value_serializer=lambda m: json.dumps(m).encode("utf-8"),
    )
    while True:
        print("== Sending events...")
        producer.send(
            os.environ.get("TOPIC_NAME", "example_topic"),
            value={"user": "doge@doge.com"},
            headers=[
                ("event_name", b"user_registered"),
            ],
        )
        producer.send(
            "example_topic",
            value={"user": "doge@doge.com", "device": "iPhone"},
            headers=[
                ("event_name", b"user_logged_in"),
            ],
        )
        sleep(5)


if __name__ == "__main__":
    bootstrap()
    main()
