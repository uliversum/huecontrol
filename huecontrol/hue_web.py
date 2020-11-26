import argparse
import configparser
import logging
import os
import sys

from bottle import route, run

import huecontrol.hue as hue  # import like this to allow egg to find the hue package after installation

hueControl = hue.HueControl()


@route('/lighton')
def light_on():
    hueControl.on()
    return 'light on!'


@route('/lightoff')
def light_off():
    hueControl.off()
    return 'light off!'


@route('/lightrandom')
def light_random():
    hueControl.do_random()
    return 'light random!'


def main(args=sys.argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--port",
                        default=8080,
                        type=int,
                        help="port of web interface")
    args = parser.parse_args()
    run(host='0.0.0.0', port=args.port, debug=True)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
