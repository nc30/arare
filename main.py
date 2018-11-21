#!/usr/bin/env python3
# coding: utf-8

from logging import getLogger
logger = getLogger('arare')


import time
import datetime
import os
import sys
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json

CHECK_SPAN = 10
THING_NAME = 'arare'
ENDPOINT = 'a3gt2cb172okvl-ats.iot.ap-northeast-1.amazonaws.com'
ROOTCA = '/home/pi/AmazonRootCA1.pem'
PRIVATE = '/home/pi/ebf86ded56-private.pem.key'
CERT = '/home/pi/ebf86ded56-certificate.pem.crt'


def cb(client, userdata, message):
    r = json.loads(message.payload.decode('utf-8'))

    try:
        global CHECK_SPAN
        CHECK_SPAN = int(r['state']['check_span'])
    except KeyError:
        pass

if __name__ == '__main__':
    from logging import StreamHandler, DEBUG
    logger.seLevel(DEBUG)
    logger.addHandler(StreamHandler(stream=sys.stdout))

    client = AWSIoTMQTTClient(THING_NAME)
    client.configureEndpoint(ENDPOINT, 8883)
    client.configureCredentials(ROOTCA, PRIVATE, CERT)

    client.configureAutoReconnectBackoffTime(1, 32, 20)
    client.configureOfflinePublishQueueing(-1)
    client.configureDrainingFrequency(2)
    client.configureConnectDisconnectTimeout(300)
    client.configureMQTTOperationTimeout(10)

    client.subscribe('$aws/things/'+THING_NAME+'/shadow/update/delta', 1, cb)
    client.connect(60)

    import threading
    from arare import door

    d = threading.Thread(target=door.main, kwargs={"client": client}, daemon=True)
    d.start()

    from arare import dashscan
    d = threading.Thread(target=door.main, kwargs={"client": client}, daemon=True)
    d.start()

    while True:
        try:
            shadow = {
                "state": {
                    "reported": {
                        "date": time.time(),
                        "check_span": CHECK_SPAN
                    }
                }
            }


            client.publish('$aws/things/'+THING_NAME+'/shadow/update', json.dumps(shadow), 1)

        except IOError:
            # this is connection error to enviro phat
            time.sleep(CHECK_SPAN)
            continue

        except Exception as e:
            logger.exception(e)

        time.sleep(CHECK_SPAN)
