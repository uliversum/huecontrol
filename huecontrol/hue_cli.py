#!/usr/bin/env python3

import cmd
import configparser
import logging
import os
import sys

try:
    import huecontrol.hue as hue # import like this to allow egg to find the hue package after installation
except:
    import hue


class HueCmd(cmd.Cmd):
    intro = 'Welcome to the huecontrol. Type help or ? to list commands.\n'
    prompt = '(light) '

    def __init__(self, hueControl):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.hueControl = hueControl
        cmd.Cmd.__init__(self)

    # ----- basic commands -----
    def do_random(self, arg):
        'Set bulbs to random colors.'
        self.hueControl.do_random()

    def do_blue(self, arg):
        'Set color of all bulbs to blue.'
        BLUE = (0.15, 0)
        self.hueControl.color_xy(BLUE)

    def do_red(self, arg):
        'Set color of all bulbs to red.'
        RED = (0.7, 0.25)
        self.hueControl.color_xy(RED)

    def do_green(self, arg):
        'Set color of all bulbs to green.'
        GREEN = (0.15, 0.825)
        self.hueControl.color_xy(GREEN)

    def do_yellow(self, arg):
        'Set color of all bulbs to yellow.'
        YELLOW = (0.5, 0.5)
        self.hueControl.color_xy(YELLOW)

    def do_brightest(self, arg):
        'Sets maximum brightness for all bulbs.'
        self.hueControl.brightness(255)

    def do_on(self, arg):
        'Switches all bulbs on.'
        self.hueControl.on()

    def do_off(self, arg):
        'Switches all bulbs off.'
        self.hueControl.off()

    def do_toggle(self, arg):
        'Toggle bulbs on or off.'
        self.hueControl.toggle()

    def do_kelvin(self, arg):
        'Set the color temperature of the light, in units of Kelvin [2000-6500]. usage: kelvin 3500'
        self.hueControl.kelvin(int(arg))

    def do_xy(self, arg):
        'Sets the color temperature according to CIE 1931 with two floats. e.g. the value for red is : xy 0.7 0.25'
        self.hueControl.color_xy(parse_float(arg))

    def do_quit(self, arg):
        'Quits the program and exit.'
        print('Thank you for using ' + self.__class__.__name__)
        return True

    def precmd(self, line):
        line = line.lower()
        return line


def parse_float(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(float, arg.split()))


def create_color_handler(format):
    stream_handler = logging.StreamHandler()
    try:
        import colorlog
        stream_handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s' + format))
    except ImportError:
        # if colorlog module is not installed use default Formatter
        stream_handler.setFormatter(logging.Formatter(format))
    return stream_handler


def main(args=sys.argv):
    NAMESPACE = ' %(module)s.%(name)s.%(funcName)s'
    FORMAT = '%(asctime)s %(levelname)-8s ' + NAMESPACE + ': %(message)s'

    color_handler = create_color_handler(FORMAT)

    LOGFILENAME = sys.argv[0].replace('.py','') + '.log'
    file_handler = logging.FileHandler(LOGFILENAME, encoding='utf-8')

    logging.basicConfig(level=logging.DEBUG, format=FORMAT, handlers=[color_handler, file_handler])
    log = logging.getLogger(__name__)

    hueControl = hue.HueControl()
    return_code = HueCmd(hueControl).cmdloop()

    logging.shutdown()
    return return_code


if __name__ == '__main__':
    sys.exit(main(sys.argv))
