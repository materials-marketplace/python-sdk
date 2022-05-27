import base64
import json
from typing import Dict

from marketplace.message_broker.models.request_message import RequestMessage
from marketplace.message_broker.models.response_message import ResponseMessage
from marketplace.message_broker.rpc_server import RpcServer


def my_endpoint_callback(
    request_message: RequestMessage, request_headers: Dict[str, str]
) -> ResponseMessage:
    print("Routing to endpoint %r..." % request_message.endpoint)
    result = len(request_message.body) if request_message.body else 0
    response = {"numberOfKeysInPayload": str(result)}
    print("Done!")
    response_message = ResponseMessage(
        response_code=200,
        body_base64=base64.b64encode(json.dumps(response)).decode(),
        headers={"Content-Type": "application/json"},
    )
    return response_message


rpc_server = RpcServer(
    host="www.materials-marketplace.eu",
    application_id="<application-id>",
    application_secret="<application-secret>",
    endpoint_callback=my_endpoint_callback,
)
rpc_server.consume_messages()
