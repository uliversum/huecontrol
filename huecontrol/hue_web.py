import configparser
import logging
import os
import sys

from bottle import route, run

import huecontrol.hue as hue # import like this to allow egg to find the hue package after installation

hueControl = None


@route('/lighton')
def light_on():
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.huecontrol/huecontrol.conf'))

    ipAddressBridge = config['DEFAULT']['IpAddressBridge']
    hueControl = hue.HueControl(ipAddressBridge)
    hueControl.on()
    return 'light on!'


@route('/lightoff')
def light_off():
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.huecontrol/huecontrol.conf'))

    ipAddressBridge = config['DEFAULT']['IpAddressBridge']
    hueControl = hue.HueControl(ipAddressBridge)
    hueControl.off()
    return 'light off!'


@route('/lightrandom')
def light_random():
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.huecontrol/huecontrol.conf'))

    ipAddressBridge = config['DEFAULT']['IpAddressBridge']
    hueControl = hue.HueControl(ipAddressBridge)
    hueControl.do_random()
    return 'light random!'


def main(args=sys.argv):
    run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
