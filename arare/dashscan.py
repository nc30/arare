# coding: utf-8

from logging import getLogger
logger = getLogger(__name__)


from scapy.all import sniff, ARP
import json

TOPIC = 'stat/arare/dash'

MACS = {
    '00:fc:8b:3d:31:dc': {
        'name': 'wanda'
    },
    'fc:65:de:83:dc:31': {
        'name': 'wanda'
    },

}

import time
ttlcache = {}
def is_locked(mac, lockIfEnable):
    try:
        if ttlcache[mac] + 3 > time.time():
            return False
    except KeyError:
        pass

    if lockIfEnable:
        ttlcache[mac] = time.time()
    return True


def main(client):
    def arp_monitorCB(packet):
        if ARP in packet and packet[ARP].op in (1,2):
            arp_mac = packet.sprintf("%ARP.hwsrc%")
            #logger.debug('get arp packet %s', arp_mac)
            for mac, val in MACS.items():
                if mac == arp_mac:
                    # logger.debug('hit %s (%s)', val['name'], mac)

                    if not is_locked(mac, True):
                        logger.debug('ttl disable. skip')
                        break

                    param = {
                        'mac': arp_mac,
                        'time': time.time(),
                        'name': val['name']
                    }
                    client.publish(TOPIC, json.dumps(param), 1)
                    break

    sniff(prn=arp_monitorCB, filter="arp", store=0)
