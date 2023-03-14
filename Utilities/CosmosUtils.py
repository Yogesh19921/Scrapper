from azure.cosmos import CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential

import logging as logger

ENDPOINT = "https://scraping-grouping.documents.azure.com:443/"
DATABASE_NAME = "Scraping"
CONTAINER_NAME = "Grouping"
key_path = PartitionKey(path="/ASIN")
credential = DefaultAzureCredential()
client = CosmosClient(url=ENDPOINT, credential=credential)
database = client.create_database_if_not_exists(id=DATABASE_NAME)
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME, partition_key=key_path, offer_throughput=400
)


def insert_entry(metadata):
    try:
        container.create_item(metadata)
    except Exception as e:
        logger.error("Insert failed for object")
        print(metadata)