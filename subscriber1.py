import os

from bootstrap import bootstrap
from pubsub.event import UserLoggedIn, UserRegistered
from pubsub.subscriber import KafkaSubscriber


def on_user_registered(event: UserRegistered) -> None:
    print("====")
    print("Received user registration event!")
    print(f"Data: {event.data}")
    print(f"Metadata: {event.metadata}")


def on_user_logged_in(event: UserLoggedIn) -> None:
    print("====")
    print("Received user login event!")
    print(f"Data: {event.data}")
    print(f"Metadata: {event.metadata}")


def main() -> None:
    subscriber = KafkaSubscriber(
        topic=os.environ.get("TOPIC_NAME", "example_topic"),
        subscriber_name="subscriber_1",
        broker_address=os.environ.get("BROKER_ADDRESS", "localhost:9092"),
    )

    subscriber.subscribe(UserRegistered, on_user_registered)
    subscriber.subscribe(UserLoggedIn, on_user_logged_in)
    subscriber.listen()


if __name__ == "__main__":
    bootstrap()
    main()
