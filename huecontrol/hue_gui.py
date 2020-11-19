#!/usr/bin/env python3
# -*- coding: utf-8; -*-

import configparser
import errno
import os
import os.path
import logging
import sys
sys.path.insert(0, "..")  # load local implementation

import PyQt5
from PyQt5.QtWidgets import QWidget, QDialog, QColorDialog, QApplication, QSystemTrayIcon, QMessageBox, QMenu, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon, QColor

import huecontrol
from huecontrol import hue
from huecontrol import images


class MyColorInputDialog(QColorDialog):
    def __init__(self, hueControl):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.info('')
        super().__init__()
        self.hueControl = hueControl
        self.setOption(QColorDialog.NoButtons, True)
        self.setOption(QColorDialog.ShowAlphaChannel, False)
        self.currentColorChanged.connect(self.on_currentColorChanged)

    def on_currentColorChanged(self, color):
        self.log.info('' + str(color.name()))
        self.hueControl.color_rgb(color.redF(), color.greenF(), color.blueF())


class SystrayApp(QWidget):

    def __init__(self, hueControl):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.info('')
        super().__init__()
        self.hueControl = hueControl
        self.left = 800
        self.top = 500
        self.width = 0
        self.height = 0
        self.setGeometry(self.left, self.top, self.width, self.height)

    def toggleAction(self):
        self.log.info('')
        self.hueControl.toggle()

    def colorAction(self):
        self.log.info('')
        dialog = MyColorInputDialog(self.hueControl)
        self.show()
        dialog.exec()
        self.hide()

    def blueAction(self):
        self.log.info('')
        BLUE = (0.15, 0)
        self.hueControl.color_xy(BLUE)

    def redAction(self):
        self.log.info('')
        RED = (0.7, 0.25)
        self.hueControl.color_xy(RED)

    def yellowAction(self):
        self.log.info('')
        YELLOW = (0.5, 0.5)
        self.hueControl.color_xy(YELLOW)

    def randomAction(self):
        self.log.info('')
        self.hueControl.do_random()

    def aboutAction(self):
        self.log.info('')
        msg_box = QMessageBox()
        message = 'License: GPLv3\r\nIcons: https://icons8.com/'
        msg_box.setText(message)
        self.show()
        _ = msg_box.exec()
        self.hide()

    def exitAction(self):
        self.log.info('')
        QApplication.exit()


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

    LOGFILENAME = os.path.join(os.getenv('HOME'), 'hue_gui.log')
    file_handler = logging.FileHandler(LOGFILENAME, encoding='utf-8')

    logging.basicConfig(level=logging.DEBUG, format=FORMAT, handlers=[color_handler, file_handler])
    log = logging.getLogger(__name__)

    app = QApplication(args)

    trayIcon = QSystemTrayIcon(QIcon(':/icons8-light-on-96.png'), app)

    hueControl = hue.HueControl()
    systray = SystrayApp(hueControl)

    menu = QMenu()
    toggleAction = menu.addAction('on/off')
    toggleAction.triggered.connect(systray.toggleAction)

    colorAction = menu.addAction('color')
    colorAction.triggered.connect(systray.colorAction)

    blueAction = menu.addAction('blue')
    blueAction.triggered.connect(systray.blueAction)

    redAction = menu.addAction('red')
    redAction.triggered.connect(systray.redAction)

    yellowAction = menu.addAction('yellow')
    yellowAction.triggered.connect(systray.yellowAction)

    randomAction = menu.addAction('random')
    randomAction.triggered.connect(systray.randomAction)

    aboutAction = menu.addAction('about')
    aboutAction.triggered.connect(systray.aboutAction)

    exitAction = menu.addAction('Exit')
    exitAction.triggered.connect(systray.exitAction)

    trayIcon.setContextMenu(menu)
    trayIcon.show()

    return_code = app.exec_()

    logging.shutdown()
    return return_code


if __name__ == '__main__':
    sys.exit(main(sys.argv))
