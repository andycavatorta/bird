import os
import queue
import threading
import time
import serial
import shelve
import socket
import sys
import zmq


class Motor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        serial_device_path = "/dev/serial/by-id/usb-Roboteq_Motor_Controller_SDC2XXX-if00"
        self.serial = serial.Serial(
            port=serial_device_path,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_NONE,
        )
        time.sleep(1) # give serial a moment
        self.start()

    def add_to_queue(
            self, 
            serial_command, 
            event=None,
            callback=None):
        if event is not None:
            event.clear()
        self.queue.put((serial_command, event, callback))

    def _readSerial_(self):
        resp_char = " "
        resp_str = ""
        while ord(resp_char) != 13:
            resp_char = self.serial.read(1)
            resp_str += resp_char.decode('utf-8')
        resp_str = resp_str[:-1] # trim /r from end
        resp_l = resp_str.split('=')
        return resp_l

    def run(self):
        while True:
            serial_command, event, callback = self.queue.get(block=True, timeout=None)
            self.serial.write(str.encode(serial_command +'\r'))
            resp = self._readSerial_()
            print(">>1",serial_command, resp)
            if len(resp)==1:
                if resp[0]=="+":
                    pass
                    # todo: do we need to pass affirmation?
                elif resp[0]=="-":
                    print("todo: response == '-' pass message of failure")
                else:# this is a command echo string.  now fetch command response
                    resp = self._readSerial_()
                    print(">>2",serial_command, resp)
                    if len(resp)!=2:
                        if resp == ['-']:
                            print("todo: response == '-' pass message of failure")
                    else:
                        if callback is not None:
                            callback(resp[1], event)

motor = Motor()

class Settings():
    def __init__(self):
        self.default_minimum_position = 10000
        self.default_maximum_position = 10000000
        self.default_speed = 100
        try:
            with shelve.open('settings', 'r') as shelf:
                self.minimum_position = shelf["minimum_position"]
                self.maximum_position = shelf["maximum_position"]
                self.speed = shelf["speed"]
        except Exception:
                self.minimum_position = self.default_minimum_position
                self.maximum_position = self.default_maximum_position
                self.speed = self.default_speed
                with shelve.open('settings', 'c') as shelf:
                    shelf['minimum_position'] = self.default_minimum_position
                    shelf['maximum_position'] = self.default_maximum_position
                    shelf['speed'] = self.default_speed

    def get_minimum_position(self):
        return shelf["minimum_position"]

    def get_maximum_position(self):
        return shelf["maximum_position"]

    def get_speed(self):
        return shelf["speed"]

    def set_minimum_position(self, minimum_position):
        self.minimum_position = minimum_position
        with shelve.open('settings', 'c') as shelf:
            shelf['minimum_position'] = minimum_position

    def set_maximum_position(self, maximum_position):
        self.maximum_position = maximum_position
        with shelve.open('settings', 'c') as shelf:
            shelf['maximum_position'] = self.default_maximum_position

    def set_speed(self, speed):
        self.speed = speed
        with shelve.open('settings', 'c') as shelf:
            shelf['speed'] = self.default_speed

settings = Settings()

class Receive_Commands_And_Settings(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5555")
        self.start()

    def run(self):
        while True:
            action, value = socket.recv_json()
            print("Received request: %s" % action, value)
            if action == b"set_minimum_position":
                settings.set_minimum_position(int(value))

            if action == b"set_maximum_position":
                settings.set_maximum_position(int(value))

            if action == b"set_speed":
                settings.set_speed(int(value))
                speed = value # assume for now that motor control speed range is 0-255 and input range is 0-255
                serial_command = "!S {} {}".format(1, speed)
                motor.add_to_queue(serial_command)

            if action == b"set_position":
                range_of_positions = settings.get_maximum_position() - settings.get_minimum_position()
                position_increment_size = int(range_of_positions / 255.0)
                destination_position = (value * position_increment_size) + settings.get_minimum_position()
                serial_command = "!PR {} {}".format(1, destination_position)
                motor.add_to_queue(serial_command)

            socket.send(b"received")

receive_commands_and_settings = Receive_Commands_And_Settings()
