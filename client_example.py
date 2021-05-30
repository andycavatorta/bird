import json
import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def send_to_server(action, value):
    action_value_json = json.dumps([action, value])
    socket.send(action_value_json)
    print(socket.recv())
