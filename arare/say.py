# coding: utf-8
from logging import getLogger
logger = getLogger(__name__)

import subprocess

def createWave(t, path):
    if isinstance(t, str):
        t = t.encode()

    open_jtalk = ['open_jtalk']
    mech = ['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice = ['-m','/usr/share/hts-voice/mei/mei_normal.htsvoice']
    speed = ['-r','1.0']
    outwav = ['-ow', path]

    cmd = open_jtalk + mech + htsvoice + speed + outwav
    logger.debug(cmd)
    c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    c.stdin.write(t)
    c.stdin.close()
    c.wait()


def play(path):
    cmd = ['aplay', path]
    subprocess.call(cmd)

def jtalk(t, path):
    createWave(t, path)
    play(path)
