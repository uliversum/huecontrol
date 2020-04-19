import phue
import logging
import random
try:
    import huecontrol.rgb_cie as rgb_cie
except:
    import rgb_cie


class HueControl():
    def __init__(self, ip):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.info('Using ip address: ' + ip)
        self.bridge = phue.Bridge(ip)
        self.bridge.connect()
        self.bulbs = self.bridge.lights
        self.color_helper = rgb_cie.ColorHelper()
        random.seed()

    def do_random(self):
        self.log.info('')
        self.on()
        for bulb in self.bulbs:
            bulb.on = True
            bulb.brightness = 254
            bulb.xy = [random.random(), random.random()]

    def color_rgb(self, red, green, blue):
        self.log.info('red: ' + str(red) + ' green: ' + str(green) + ' blue: ' + str(blue))
        self.on()
        xy = self.color_helper.getXYPointFromRGB(red, green, blue)
        color_xy = (xy.x, xy.y)
        self.color_xy(color_xy)

    def color_xy(self, color):
        self.log.info(str(color))
        for bulb in self.bulbs:
            bulb.on = True
            bulb.xy = color

    def brightness(self, brightness):
        self.log.info('')
        self.on()
        for bulb in self.bulbs:
            bulb.on = True
            bulb.brightness = brightness

    def on(self):
        self.log.info('on')
        for bulb in self.bulbs:
            bulb.on = True

    def off(self):
        self.log.info('')
        for bulb in self.bulbs:
            bulb.on = False

    def toggle(self):
        self.log.info('')
        for bulb in self.bulbs:
            bulb.on = not bulb.on

    def kelvin(self, kelvin):
        self.log.info('')
        self.on()
        for bulb in self.bulbs:
            bulb.on = True
            bulb.colortemp_k = kelvin
