#!/usr/bin/env python

import os
import pika
import json

from logger import logger

class Queue(object):

  def __init__(self,
      host=os.environ.get('QUEUE_HOST', 'localhost'),
      port=os.environ.get('QUEUE_PORT', 5672),
      username=os.environ.get('QUEUE_USERNAME', 'quest'),
      password=os.environ.get('QUEUE_PASSWORD', 'quest')
    ):

    logger.info(f"Connecting to {host}:{port} as user {username}/{password}")

    self.connection = pika.BlockingConnection(
        pika.ConnectionParameters(
        host,
        port,
        username,
        pika.PlainCredentials(username, password)
      )
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
            raise Exception(f"No handler for: {k} !")

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
      logger.info("Stop consuming...")
      self.channel.stop_consuming()
