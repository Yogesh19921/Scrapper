from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.identity import DefaultAzureCredential

FULLY_QUALIFIED_NAMESPACE = "scrap-url-list.servicebus.windows.net"
TOPIC_NAME = "items"
SUBSCRIPTION_NAME = "url-list-subscription"

credential = DefaultAzureCredential()
servicebus_client = ServiceBusClient(
    fully_qualified_namespace=FULLY_QUALIFIED_NAMESPACE,
    credential=credential,
    logging_enable=True)
sender = servicebus_client.get_topic_sender(topic_name=TOPIC_NAME)
receiver = servicebus_client.get_subscription_receiver(
    topic_name=TOPIC_NAME,
    subscription_name=SUBSCRIPTION_NAME
)


def send_message(body):
    message = ServiceBusMessage(body)
    sender.send_messages(message)
    print("Sent message")


def get_message(count=1):
    received_msgs = receiver.receive_messages(max_message_count=count, max_wait_time=5)
    return received_msgs


def complete_message(message):
    receiver.complete_message(message)