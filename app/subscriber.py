#/usr/bin/env python3

import os
import logging

from amqp import AMQP


log_level = os.environ.get('LOG_LEVEL', 'ERROR')

logging.basicConfig(
    level=logging.getLevelName(log_level),
    format='%(asctime)s %(levelname)s %(message)s')

logger = logging.getLogger()


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

