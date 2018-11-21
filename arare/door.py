# coding: utf-8

from logging import getLogger
logger = getLogger(__name__)

import serial
import twe_parser
import time
import json

SERIAL = '/dev/ttyAMA0'
TOPIC = 'door/1/state'

def main(client):
    s = serial.Serial('/dev/ttyAMA0', 115200)

    while True:
        try:
            line = s.readline()
            r = twe_parser.parse(line)

            if not r.enable:
                continue

            if r.DID == '0x0':
                param = {
                    'is_open': r.D1,
                    'voltage': r.VOLTAGE,
                    'timestamp': time.time()
                }
                client.publish(TOPIC, json.dumps(param), 0)

        finally:
            logger.info('stop')
            serial.close()
