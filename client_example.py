import json
import zmq

context = zmq.Context()
zmq_socket = context.socket(zmq.REQ)
zmq_socket.connect("tcp://192.168.0.29:5555")

def send_to_server(action, value):
    zmq_socket.send_json([action, value])
    print("a1")
    print(zmq_socket.recv())
    print("a2")
