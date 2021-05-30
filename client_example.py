import json
import zmq

context = zmq.Context()

#  zmq_socket to talk to server
print("Connecting to server…")
zmq_socket = context.socket(zmq.REQ)
zmq_socket.connect("tcp://localhost:5555")

def send_to_server(action, value):
    #action_value_json = json.dumps([action, value])
    #zmq_socket.send(action_value_json)
    zmq_socket.send_json([action, value])
    print(zmq_socket.recv())
