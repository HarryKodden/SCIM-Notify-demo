#/usr/bin/env python3

from __future__ import print_function

import os
import json
import requests
import base64
import logging

log_level = os.environ.get('LOG_LEVEL', 'ERROR')

logging.basicConfig(
    level=logging.getLevelName(log_level),
    format='%(asctime)s [BROKER] %(levelname)s %(message)s')

logger = logging.getLogger()

class Broker(object):

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
      logger.debug(f"BROKER: {method} {url} {json.dumps(payload)}")

      response = requests.request(method, url, data=json.dumps(payload), headers=headers, verify=self.verify)

      logger.debug(f"[{response.status_code}] {method} {url}...")

      return json.loads(response.text)

    except requests.exceptions.SSLError:
      logger.error("SSL Validation error.")

    return None

  def enable_service(self, service_name, service_password):

    if (service_name == ""):
      raise Exception("Service name can not be blank !")

    if (service_password == ""):
      raise Exception("Service password can not be blank !")

    logger.info(f"Enabling service: '{service_name}'...")
    self.api(f"/api/vhosts/{service_name}", method='PUT')

    logger.info(f"Adding credentials for service: '{service_name}'...")
    self.api(f"/api/users/{service_name}", method='PUT', payload={ 
        "password": service_password, 
        "tags": ""
      }
    )

    logger.info(f"Adding permissions for service: '{service_name}'...")
    self.api(f"/api/permissions/{service_name}/{service_name}", method='PUT', payload={ 
        "configure": ".*", 
        "write": ".*",
        "read": ".*"
      }
    )

    logger.info(f"Service: '{service_name}' is now enabled !")

  def notify_service(self, service, data):
    for k,v in data.items():
      logger.info(f"Notify {service} for update on '{k}' value: '{v}'...")
    
    return self.api(f"/api/exchanges/{service}/amq.topic/publish", method='POST', payload={
        "properties": {},
        "routing_key": "",
        "payload": json.dumps(data),
        "payload_encoding": "string"
      }
    )['routed'] == True


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

    for service in services:
      try:
        service_name, service_password = [x.strip() for x in service.split('=')]
        broker.enable_service(service_name, service_password)
      except Exception as e:
        logger.error(f"Configuration error: {str(e)}")
