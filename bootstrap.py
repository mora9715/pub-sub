import os
from time import sleep

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import NoBrokersAvailable, TopicAlreadyExistsError


def bootstrap() -> None:
    """Wait for a broker to get up and running, creating a default topic after that."""
    while True:
        try:
            print("== Trying to create a topic...")
            admin_client = KafkaAdminClient(
                bootstrap_servers=os.environ.get("BROKER_ADDRESS", "localhost:9092"),
                client_id="user",
            )

            admin_client.create_topics(
                new_topics=[
                    NewTopic(
                        name=os.environ.get("TOPIC_NAME", "example_topic"),
                        num_partitions=1,
                        replication_factor=1,
                    )
                ],
                validate_only=False,
            )
            print("== Created topic successfully!")
        except TopicAlreadyExistsError:
            print("== Topic already exists. Skipping...")
            break
        except NoBrokersAvailable:
            print("== Broker is not available yet. Retrying...")
            sleep(5)
        else:
            break
