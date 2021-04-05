"""
HEAD Mouse for windows
"""

import math
import multiprocessing
from threading import Thread

import win32api, win32con
import serial, sys, time
from configparser import ConfigParser
from global_hotkeys import *

config = ConfigParser()
config.read("config.ini")


def cfg(key):
    return config["APP"].get(key)


# DATA looks like this
# >>>X:-0.01,	Y:-0.00,	Z:0.04


sensitivity = int(cfg("sensitivity"))
filter = int(cfg("filter"))

ser = serial.Serial('COM' + cfg("COM"))
print(f"Opening COM{cfg('COM')} ")


class Readings:
    x = 0
    y = 0
    z = 0


def _get_single_reading_value_from_string(read_string):
    data = read_string.split(b":")
    return float(data[1])


def read_data() -> Readings:
    r = Readings()
    line = ser.readline()

    try:
        readings_tab = line.split(b",")
        if len(readings_tab) > 3:
            return
        r.x = _get_single_reading_value_from_string(readings_tab[0])
        r.y = _get_single_reading_value_from_string(readings_tab[1])
        r.z = _get_single_reading_value_from_string(readings_tab[2])
        return r
    except Exception as e:
        print("error")
        return r


class Mouse:
    x = 0
    y = 0
    is_right_down = False
    is_left_down = False
    is_active = True

    def move(self):
        win32api.SetCursorPos((self.x, self.y))

    def left_down(self):
        self.is_left_down = True
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, self.x, self.y, 0, 0)

    def left_up(self):
        self.is_left_down = False
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, self.x, self.y, 0, 0)

    def right_down(self):
        self.is_right_down = True
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, self.x, self.y, 0, 0)

    def right_up(self):
        self.is_right_down = False
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, self.x, self.y, 0, 0)


def is_key_pressed(key='Q'):
    return win32api.GetAsyncKeyState(ord(key))


class Resolution:
    width: 0
    height: 0

    def __init__(self):
        self.width = win32api.GetSystemMetrics(0)
        self.height = win32api.GetSystemMetrics(1)

    def __str__(self):
        return f' SCRREN SIZE: \nWidth{self.width}\nHeight: {self.height}'


resolution = Resolution()

mouse = Mouse()
print(resolution)


def center():
    mouse.x = int(resolution.width / 2)
    mouse.y = int(resolution.height / 2)
    mouse.move()


center()
print("HEADMOUSE!")
time.sleep(0.5)

x_modifier = float(cfg("x-axis-modifier"))
y_modifier = float(cfg("y-axis-modifier"))


def quit():
    print("BYE BYE")
    ser.close()
    exit(0)


def toggle_mouse_active():
    mouse.is_active = not mouse.is_active


def click():
    mouse.left_down()
    mouse.left_up()


def right_click():
    mouse.right_down()
    mouse.right_up()


def drag():
    if not mouse.is_left_down:
        mouse.left_down()
    else:
        mouse.left_up()


def increase_sensitivity():
    global sensitivity
    sensitivity += 10


def decrease_sensitivity():
    global sensitivity
    sensitivity -= 10


bindings = [
    [["control", "shift", "q"], None, quit],
    [["control", "shift", "a"], None, toggle_mouse_active],
    [["control", "shift", "z"], None, click],
    [["control", "shift", "x"], None, right_click],
    [["control", "shift", "w"], None, center],
    [["control", "shift", "1"], None, decrease_sensitivity],
    [["control", "shift", "2"], None, increase_sensitivity],
]
register_hotkeys(bindings)

start_checking_hotkeys()
# thread = Thread(target=start_checking_hotkeys)
# thread.start()

while True:
    r = read_data()
    x_val = 0
    if cfg("x-axis") == "x":
        x_val = r.x
    elif cfg("x-axis") == "y":
        x_val = r.y
    else:
        x_val = r.z

    y_val = 0
    if cfg("y-axis") == "x":
        y_val = r.x
    elif cfg("y-axis") == "y":
        y_val = r.y
    else:
        y_val = r.z

    if mouse.is_active:
        if filter < math.fabs(x_val):
            mouse.x = int(mouse.x + (x_modifier * (x_val / sensitivity)))
        if filter < math.fabs(y_val):
            mouse.y = int(mouse.y + (y_modifier * (y_val / sensitivity)))
        mouse.move()

    # if win32api.GetAsyncKeyState(win32con.VK_LCONTROL) and win32api.GetAsyncKeyState(
    #         win32con.VK_LSHIFT) and win32api.GetAsyncKeyState(ord('Z')):
    #     if not mouse.is_left_down:
    #         mouse.left_down()
    # else:
    #     if mouse.is_left_down:
    #         mouse.left_up()
    #
    # if win32api.GetAsyncKeyState(win32con.VK_LCONTROL) and win32api.GetAsyncKeyState(
    #         win32con.VK_LSHIFT) and win32api.GetAsyncKeyState(ord('X')):
    #     if not mouse.is_right_down:
    #         mouse.right_down()
    # else:
    #     if mouse.is_right_down:
    #         mouse.right_down()
    #
    # if win32api.GetAsyncKeyState(win32con.VK_LCONTROL) and win32api.GetAsyncKeyState(
    #         win32con.VK_LSHIFT) and win32api.GetAsyncKeyState(ord('W')):
    #         mouse.left_down()
    #         mouse.left_up()
    #
    # if win32api.GetAsyncKeyState(win32con.VK_LCONTROL) and win32api.GetAsyncKeyState(
    #         win32con.VK_LSHIFT) and win32api.GetAsyncKeyState(ord('E')):
    #     center()
    # if win32api.GetAsyncKeyState(win32con.VK_LCONTROL) and win32api.GetAsyncKeyState(
    #         win32con.VK_LSHIFT) and win32api.GetAsyncKeyState(ord('Q')):
    #     ser.close()
    #     print("BYE BYE")
    #     exit(0)
    #
    # if win32api.GetAsyncKeyState(win32con.VK_LCONTROL) and win32api.GetAsyncKeyState(
    #         win32con.VK_LSHIFT) and win32api.GetAsyncKeyState(ord('A')):
    #
    #     mouse.is_active = not mouse.is_active
    #     time.sleep(0.5)
