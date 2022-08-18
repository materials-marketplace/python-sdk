import json

from marketplace_standard_app_api.models.message_broker import (
    MessageBrokerRequestModel,
    MessageBrokerResponseModel,
)

from marketplace.message_broker.rpc_server import RpcServer


def my_message_handler(
    request_message: MessageBrokerRequestModel,
) -> MessageBrokerResponseModel:
    print("Routing to endpoint %r..." % request_message.endpoint)
    payload = json.loads(request_message.body) if request_message.body else {}
    result = len(payload)
    response = {"numberOfKeysInPayload": str(result)}
    print("Done!")
    response_message = MessageBrokerResponseModel(
        status_code=200,
        body=json.dumps(response),
        headers={"Content-Type": "application/json"},
    )
    return response_message


rpc_server = RpcServer(
    host="staging.materials-marketplace.eu",
    application_id="dc67d85e-7945-49fa-bf85-3159a8358f85",
    application_secret="2366c94a-1361-4c85-9016-e16b1fe7dfa1",
    message_handler=my_message_handler,
)
rpc_server.consume_messages()
