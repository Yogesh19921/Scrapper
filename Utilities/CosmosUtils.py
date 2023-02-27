from azure.cosmos import CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential

ENDPOINT = "https://scraping-grouping.documents.azure.com:443/"
DATABASE_NAME = "Scraping"
CONTAINER_NAME = "Groups"
key_path = PartitionKey(path="/ASIN")


def get_container():
    credential = DefaultAzureCredential()
    client = CosmosClient(url=ENDPOINT, credential=credential)
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
    c = database.create_container_if_not_exists(
        id=CONTAINER_NAME, partition_key=key_path, offer_throughput=400
    )
    return c


container = get_container()


def insert_entry(metadata):
    container.create_item(metadata)