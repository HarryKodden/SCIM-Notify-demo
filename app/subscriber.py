#/usr/bin/env python3

import os

from support import AMQP, logger

def user(id):
  logger.info(f"[USER:{id}] Notification received !")

def group(id):
  logger.info(f"[GROUP:{id}] Notification received !")


if __name__ == "__main__":

  AMQP(os.environ['URI']).subscribe({
      'user': user,
      'group': group
    }
  )

