#/usr/bin/env python3

from __future__ import print_function

import os
import sys
import json
import requests
import base64
import random
import time
import logging

log_level = os.environ.get('LOG_LEVEL', 'ERROR')

logging.basicConfig(
    level=logging.getLevelName(log_level),
    format='%(asctime)s %(levelname)s %(message)s')

logger = logging.getLogger()

class Control(object):

  def __init__(self, server, port=None, username='guest', password='guest', verify=True, cacert=None):
    self.server = server
    if port:
      self.server += f":{port}"

    self.authorization = "Basic " + base64.b64encode(f"{username}:{password}".encode()).decode()

    if verify and cacert:
      self.verify = cacert
    else:
      self.verify = verify

  def __enter__(self):
    return self

  def __exit__(self, exception_type, exception_value, traceback):
    """ Nothing to do here """
    pass

  def api(self, uri, method='GET', payload=None):
    url = self.server + uri
    
    headers = {}

    if payload:
      headers['content-type'] = "application/json"

    if self.authorization:
      headers['Authorization'] = self.authorization
    
    try:
      logger.debug(f"API: {method} {url} {json.dumps(payload)}")

      response = requests.request(method, url, data=json.dumps(payload), headers=headers, verify=self.verify)

      logger.debug(f"[{response.status_code}] {method} {url}...")

      if (response.text > ''):
        return response.json()

    except requests.exceptions.SSLError:
      logger.error("SSL Validation error.")

    return None


my_control = Control(
  os.environ.get("API_HOST", "http://localhost"),
  port = os.environ.get("API_PORT", None),
  username = os.environ.get('API_USER', "guest"),
  password = os.environ.get('API_PASS', "guest")
)

def enable_services(services):

  for service in services:

    try:
      service_name, service_password = [x.strip() for x in service.split('=')]

      if (service_name == ""):
        raise Exception("Service name can not be blank !")

      if (service_password == ""):
        raise Exception("Service password can not be blank !")

    except Exception as e:
      logger.error(f"Configuration error: {str(e)}")
      continue

    logger.info(f"Enabling service: '{service_name}'...")
    my_control.api(f"/api/vhosts/{service_name}", method='PUT')

    logger.info(f"Adding credentials for service: '{service_name}'...")
    my_control.api(f"/api/users/{service_name}", method='PUT', payload={ 
        "password": service_password, 
        "tags": ""
      }
    )

    logger.info(f"Adding permissions for service: '{service_name}'...")
    my_control.api(f"/api/permissions/{service_name}/{service_name}", method='PUT', payload={ 
        "configure": ".*", 
        "write": ".*",
        "read": ".*"
      }
    )
    logger.info(f"Service: '{service_name}' is now enabled !")
    

def notify_service(service, data):
  for k,v in data.items():
    logger.info(f"Notify {service_name} for update on '{k}' value: '{v}'...")
  
  my_control.api(f"/api/exchanges/{service}/amq.topic/publish", method='POST', payload={
      "properties": {},
      "routing_key": "",
      "payload": json.dumps(data),
      "payload_encoding": "string"
    }
  )

if __name__ == "__main__":
  services = os.environ.get("SERVICES","").split(';')

  if len(services) == 0:
    logger.error(f"No Services configured !")
    sys.exit(-1)

  enable_services(services)

  topics = ['user', 'group']

  while len(services) > 0:
    s = random.randrange(0, len(services))
    t = random.randrange(0, len(topics))

    service_name = [x.strip() for x in services[s].split('=')][0]

    if (service_name == ""):
      logger.error(f"Service name can not be blank !")
      break

    notify_service(service_name, {
      topics[t]: random.randrange(1, 99999)
    })

    time.sleep(3)