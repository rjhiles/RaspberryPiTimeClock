import socket
import pickle
from Database import TimeEntries

HOST = "192.168.0.20"
PORT = 9999


def send(data_dict):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        pickle_dict = pickle.dumps(data_dict)
        s.sendall(pickle_dict)


def send_and_recv(data_dict):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        pickle_dict = pickle.dumps(data_dict)
        s.sendall(pickle_dict)
        data = s.recv(1024)
    return pickle.loads(data)