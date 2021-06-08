import json
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
            callback=None):
        print(100)
        self.queue.put((serial_command, callback))
        print(101)

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
            print(102)
            serial_command, callback = self.queue.get(block=True, timeout=None)
            print(103)
            self.serial.write(str.encode(serial_command +'\r'))
            print(104)
            resp = self._readSerial_()
            print(105)
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
                            callback(resp[1])

motor = Motor()

while True:
    serial_command = "!MG"
    motor.add_to_queue(serial_command)

    time.sleep(1)
    serial_command = "!P 1 -1000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -43000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -1000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -43000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -1000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -43000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -1000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -43000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -1000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -43000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -1000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -43000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -1000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -43000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -1000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -43000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -1000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -43000"
    motor.add_to_queue(serial_command)
    time.sleep(6)
    serial_command = "!P 1 -0"
    motor.add_to_queue(serial_command)
    serial_command = "!EX"
    motor.add_to_queue(serial_command)
    print("starting rest period")
    time.sleep(170)
    print("10")
    time.sleep(1)
    print("9")
    time.sleep(1)
    print("8")
    time.sleep(1)
    print("7")
    time.sleep(1)
    print("6")
    time.sleep(1)
    print("5")
    time.sleep(1)
    print("4")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")


