#/usr/bin/env python3

from __future__ import print_function

import os
import json
import requests
import base64
import random
import time

from logger import logger

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

def enables_services(services):

  for service in services:
    service_name, service_password = service.split('=')
    logger.debug(f"SERVICE: {service_name} --> {service_password}")

    my_control.api(f"/api/vhosts/{service_name}", method='PUT')
    my_control.api(f"/api/users/{service_name}", method='PUT', payload={ 
        "password": service_password, 
        "tags": ""
      }
    )

    my_control.api(f"/api/permissions/{service_name}/{service_name}", method='PUT', payload={ 
        "configure": ".*", 
        "write": ".*",
        "read": ".*"
      }
    )

def notify_service(service, data):
  my_control.api(f"/api/exchanges/{service}/amq.topic/publish", method='POST', payload={
      "properties": {},
      "routing_key": "",
      "payload": json.dumps(data),
      "payload_encoding": "string"
    }
  )

if __name__ == "__main__":
  services = os.environ.get("SERVICES",[]).split(';')

  enables_services(services)

  topics = ['user', 'group']

  while len(services) > 0:
    s = random.randrange(0, len(services))
    t = random.randrange(0, len(topics))

    service_name, _ = services[s].split('=')

    notify_service(service_name, {
      topics[t]: random.randrange(1, 99999)
    })

    time.sleep(3)