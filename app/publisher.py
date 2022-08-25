#/usr/bin/env python3

from __future__ import print_function

import os
import sys
import random
import time
import logging

from broker import Broker

log_level = os.environ.get('LOG_LEVEL', 'ERROR')

logging.basicConfig(
    level=logging.getLevelName(log_level),
    format='%(asctime)s [BROKER] %(levelname)s %(message)s')

logger = logging.getLogger()

if __name__ == "__main__":

  with Broker(
    os.environ.get("BROKER_HOST", "http://localhost"),
    port = os.environ.get("BROKER_PORT", None),
    username = os.environ.get('BROKER_USER', "guest"),
    password = os.environ.get('BROKER_PASS', "guest")
  ) as broker:

    services = os.environ.get("SERVICES","").split(';')

    if len(services) == 0:
      logger.error(f"No Services configured !")
      sys.exit(-1)

    for service in services:
    
      try:
        service_name, service_password = [x.strip() for x in service.split('=')]

        if (service_name == ""):
          raise Exception("Service name can not be blank !")

        if (service_password == ""):
          raise Exception("Service password can not be blank !")

        broker.enable_service(service_name, service_password)

      except Exception as e:
        logger.error(f"Configuration error: {str(e)}")
        continue

    topics = ['user', 'group']

    while len(services) > 0:
      s = random.randrange(0, len(services))
      t = random.randrange(0, len(topics))

      service_name = [x.strip() for x in services[s].split('=')][0]

      if (service_name == ""):
        logger.error(f"Service name can not be blank !")
        break

      broker.notify_service(service_name, {
        topics[t]: random.randrange(1, 99999)
      })

      time.sleep(3)