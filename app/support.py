#!/usr/bin/env python

from __future__ import print_function

import os
import pika
import json
import logging

log_level = os.environ.get('LOG_LEVEL', 'ERROR')

logging.basicConfig(
    level=logging.getLevelName(log_level),
    format='%(asctime)s %(levelname)s %(message)s')

logger = logging.getLogger()

class AMQP(object):

  def __init__(self, uri):

    logger.info(f"Connecting to {uri}...")

    self.connection = pika.BlockingConnection(
      pika.URLParameters(uri)
    )

    self.exchange = 'amq.topic'
    self.exchange_type = 'topic'

    self.channel = self.connection.channel()
    self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type, durable=True)

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.connection.close()

  def publish(self, data, routing_key=''):
    self.channel.basic_publish(exchange=self.exchange, routing_key=routing_key, body=json.dumps(data))

  def subscribe(self, handlers, binding_key='#'):

    def callback(ch, method, properties, body):
      try:
        data = json.loads(body)

        for k in data.keys():
          if k not in handlers:
            raise Exception(f"No handler for topic: {k} !")

        for k,v in handlers.items():
          if k in data:
            v(data[k])

      except Exception as e:
        logger.error(f"Exception during consumption of {body}, exception: {str(e)}")

    queue_name = self.channel.queue_declare('', exclusive=False).method.queue
    self.channel.queue_bind(exchange=self.exchange, queue=queue_name, routing_key=binding_key)
    self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    try:
      logger.info("Start consuming...")
      self.channel.start_consuming()
    except KeyboardInterrupt:
      logger.info("Keyboard interrup received !")
    except Exception as e:
      logger.info(f"Stop consuming because: {str(e)}")

    self.channel.stop_consuming()
