import base64
import json
import logging

import pika

from .models.message import Message

logger = logging.getLogger(__name__)


class RpcServer:
    def __init__(self, host, queue_name, endpoint_callback):
        self.queue_name = queue_name
        self.endpoint_callback = endpoint_callback
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = connection.channel()

        self.channel.queue_delete(
            queue=queue_name
        )  # Delete old queue. Otherwise, first message might not be consumed.
        self.channel.queue_declare(queue=queue_name)

    def consume_messages(self):
        def callback(ch, method, properties, body):
            message = Message.parse_obj(json.loads(body.decode()))
            logger.info("Messaged received for endpoint %s" % message.endpoint)
            body_str = base64.b64decode(message.body_base64)
            body_dict = None
            if body_str:
                body_dict = json.loads(body_str)
            message.body = body_dict

            response = self.endpoint_callback(message, properties.headers)

            ch.basic_publish(
                exchange="",
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(
                    correlation_id=properties.correlation_id
                ),
                body=response,
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback)

        logger.info("Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()
