import json
import os
from time import sleep

from bootstrap import bootstrap
from pubsub.event import UserLoggedIn, UserRegistered
from pubsub.publisher import KafkaPublisher


def main() -> None:
    topic = os.environ.get("TOPIC_NAME", "example_topic")
    publisher = KafkaPublisher(
        broker_address=os.environ.get("BROKER_ADDRESS", "localhost:9092")
    )

    while True:
        print("== Sending events...")
        publisher.publish(
            UserRegistered(data={"user": "doge@doge.com"}, metadata={}), topic=topic
        )
        publisher.publish(
            UserLoggedIn(
                data={"user": "doge@doge.com", "device": "iPhone"}, metadata={}
            ),
            topic=topic,
        )
        sleep(5)


if __name__ == "__main__":
    bootstrap()
    main()
