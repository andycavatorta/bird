import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def send_to_server(action, value):
    socket.send_json([action, value])
    print(socket.recv())
