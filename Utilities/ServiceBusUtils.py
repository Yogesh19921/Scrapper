from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.identity import DefaultAzureCredential

FULLY_QUALIFIED_NAMESPACE = "scrap-url-list.servicebus.windows.net"
TOPIC_NAME = "items"

credential = DefaultAzureCredential()
servicebus_client = ServiceBusClient(
    fully_qualified_namespace=FULLY_QUALIFIED_NAMESPACE,
    credential=credential,
    logging_enable=True)
sender = servicebus_client.get_topic_sender(topic_name=TOPIC_NAME)


def send_message(body):
    message = ServiceBusMessage(body)
    sender.send_messages(message)
    print("Sent message")