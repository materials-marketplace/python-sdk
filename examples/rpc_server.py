import json
from typing import Dict

from marketplace.message_broker.models.message import Message
from marketplace.message_broker.rpc_server import RpcServer


def my_endpoint_callback(message: Message, headers: Dict[str, str]):
    print("Routing to endpoint %r..." % message.endpoint)
    result = len(message.body) if message.body else 0
    response = {"numberOfKeysInPayload": str(result)}
    print("Done!")
    return json.dumps(response)


application_id = "3a9e9445-5d59-4d74-a26a-a4cfff366a01"
rpc_server = RpcServer(
    host="www.materials-marketplace.eu",
    queue_name=application_id,
    endpoint_callback=my_endpoint_callback,
)
rpc_server.consume_messages()
