# coding: utf-8

from logging import getLogger
logger = getLogger(__name__)

from scapy.all import sniff, ARP

TOPIC = 'stat/arare/dash'

MACS = {
    '00:fc:8b:3d:31:dc': {
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
            logger.debug('get arp packet %s', arp_mac)
            for mac, val in macs.items():
                if mac == arp_mac:
                    logger.info('hit %s (%s)', val['name'], mac)

                    if not is_locked(mac, True):
                        logger.debug('ttl disable. skip')
                        break

                        client.publish(TOPIC, arp_mac, 1)
                    break

    sniff(prn=arp_monitorCB, filter="arp", store=0)
