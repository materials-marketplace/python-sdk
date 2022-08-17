import json

from marketplace_standard_app_api.models.message_broker import (
    MessageBrokerRequestModel,
    MessageBrokerResponseModel,
)

from marketplace.message_broker.rpc_server import RpcServer


def my_message_handler(
    request_message: MessageBrokerRequestModel,
) -> MessageBrokerResponseModel:
    print(
        f"Routing to endpoint {request_message.endpoint} for method {request_message.method}..."
    )
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
    host="www.materials-marketplace.eu",
    application_id="<application-id>",
    application_secret="<application-secret>",
    message_handler=my_message_handler,
)
rpc_server.consume_messages()
