#/usr/bin/env python3

from __future__ import print_function

import os
import logging

log_level = os.environ.get('LOG_LEVEL', 'ERROR')

logging.basicConfig(
    level=logging.getLevelName(log_level),
    format='%(asctime)s %(levelname)s %(message)s')

logger = logging.getLogger()
