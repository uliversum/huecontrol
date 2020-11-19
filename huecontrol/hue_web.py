import configparser
import logging
import os
import sys

from bottle import route, run

import huecontrol.hue as hue # import like this to allow egg to find the hue package after installation

hueControl = None


@route('/lighton')
def light_on():
    hueControl = hue.HueControl()
    hueControl.on()
    return 'light on!'


@route('/lightoff')
def light_off():
    hueControl = hue.HueControl()
    hueControl.off()
    return 'light off!'


@route('/lightrandom')
def light_random():
    hueControl = hue.HueControl()
    hueControl.do_random()
    return 'light random!'


def main(args=sys.argv):
    run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
