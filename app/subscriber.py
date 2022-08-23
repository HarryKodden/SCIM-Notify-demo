#/usr/bin/env python3

import os
from re import M

from logger import logger
from queue_support import Queue

def user(id):
  logger.info(f"[USER:{id}] Started...")

def group(id):
  logger.info(f"[GROUP:{id}] Started...")

handlers = {
  'user': user,
  'group': group
}

my_queue = Queue(
  host=os.environ['QUEUE_HOST'],
  port=os.environ['QUEUE_PORT'],
  username=os.environ['QUEUE_USERNAME'],
  password=os.environ['QUEUE_PASSWORD']
)

if __name__ == "__main__":
  my_queue.subscribe(handlers)
