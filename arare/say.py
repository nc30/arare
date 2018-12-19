# coding: utf-8
from logging import getLogger
logger = getLogger(__name__)

import subprocess
import datetime
import os


ALSA_VOLUME = {
    'root': 'Speaker',
    'other': 'Master'
}
OPENJTALK_DICTIONALY = '/var/lib/mecab/dic/open-jtalk/naist-jdic'
OPENJTALK_VOICE = '/usr/share/hts-voice/mei/mei_normal.htsvoice'


def createJtalkWave(text, path='/tmp/sound.wav'):
    if isinstance(text, str):
        text = text.encode()

    open_jtalk = ['open_jtalk']
    mech = ['-x', OPENJTALK_DICTIONALY]
    htsvoice = ['-m', OPENJTALK_VOICE]
    speed = ['-r','1.0']
    outwav = ['-ow', path]

    cmd = open_jtalk + mech + htsvoice + speed + outwav
    logger.debug('use command %s', cmd)

    c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    c.stdin.write(text)
    c.stdin.close()
    c.wait()

    return path


def play(path):
    cmd = ['aplay', path]
    logger.debug('use command %s', cmd)

    subprocess.call(cmd)


def jtalk(text, path='/tmp/sound.wav'):
    path = createJtalkWave(text, path)
    play(path)


def sayTime(pattern=None, path='/tmp/sound.wav'):
    if pattern is None:
        pattern = '現在時刻は、%H時%M分です'
    now = datetime.datetime.now()

    jtalk(now.strftime(pattern), path)

def changeVolume(volume):
    state = ALSA_VOLUME['other']

    # if iam root, change state is "speaker"
    if 0 == os.getuid():
        state = ALSA_VOLUME['root']

    if isinstance(volume, int):
        _changeVolume(volume, state)
        return

    raise TypeError('volume value is should integer. ('+str(volume)+ ')')

def _changeVolume(volume, state='Speaker'):
    cmd = [
        'amixer',
        'set',
        state,
        str(volume) + '%'
    ]
    subprocess.call(cmd)


if __name__ == '__main__':
    import argparse
    import logging
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    parser = argparse.ArgumentParser(description='jtalk say command')
    subParser = parser.add_subparsers()

    sayCommand = subParser.add_parser('say', help="say text")
    sayCommand.add_argument('text', metavar='text', action='store', type=str)
    sayCommand.set_defaults(handler=jtalk)

    volumeCommand = subParser.add_parser('volume', help="change volume")
    volumeCommand.add_argument('volume', action='store', type=int, help="音量　0-100")
    volumeCommand.set_defaults(handler=changeVolume)

    sayTimeCommnad = subParser.add_parser('time', help="say_time")
    sayTimeCommnad.set_defaults(handler=sayTime)

    args = parser.parse_args()

    if hasattr(args, 'handler'):
        a = [getattr(args, i) for i in dir(args) if i[0] != '_' and i != 'handler']
        args.handler(*a)
    else:
        parser.print_help()

    sys.exit(0)
