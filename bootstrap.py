import os
from time import sleep

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import NoBrokersAvailable, TopicAlreadyExistsError
from loguru import logger


def bootstrap() -> None:
    """Wait for a broker to get up and running, creating a default topic after that."""
    while True:
        try:
            logger.info("Trying to create a topic...")
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
            logger.info("Created topic successfully!")
        except TopicAlreadyExistsError:
            logger.info("Topic already exists. Skipping...")
            break
        except NoBrokersAvailable:
            logger.info("Broker is not available yet. Retrying...")
            sleep(5)
        else:
            break
