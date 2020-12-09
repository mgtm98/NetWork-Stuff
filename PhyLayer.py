import socket
import json
import threading
import time


class PhyLayer():
    
    class Frame:
        class Type:
            DATA = 0
            ACK = 1
            NAK = 2

        def __init__(self, type, seq:int, ack:int, info:list):
            self.type = type
            self.seq = seq
            self.ack = ack
            self.info = info

        def toString(self):
            out = {
                "TYPE": self.type,
                "SEQ": self.seq,
                "ACK": self.ack,
                "INFO": self.info
            }
            return json.dumps(out)

        @staticmethod
        def toFrame(json_str):
            data = json.loads(json_str)
            return PhyLayer.Frame(
                type=int(data["TYPE"]),
                seq=int(data["SEQ"]),
                ack=int(data["ACK"]),
                info=data["INFO"]
            )
    
    def __init__(self, my_host, my_listen_port, his_host, his_listen_port):
        self._buffer_from_dlink = []
        self._buffer_to_dlink = []
        self._init_sockets(my_host, my_listen_port)
        self._his_host = his_host
        self._his_listen_port = his_listen_port
        self._send_timer = threading.Timer(1, self._send_CB)

    def _init_sockets(self, host, port):
        setattr(socket.socket, "connected", False)
        self.listener_socket = socket.socket()            # Create a socket object
        self.listener_socket.bind((host, port))
        self.sender_socket = socket.socket()               # Create a socket object
        self._sender_socket_connected = False

    def add_to_buffer(self, frame):
        # print("[PhyLayer] Data added to the to_buffer ", frame.toString())
        self._buffer_from_dlink.append(frame.toString())
        # self.sender_socket.close()

    def data_available(self):
        return len(self._buffer_to_dlink) > 0

    def get_from_buffer(self):
        return self._buffer_to_dlink.pop(0)

    def _send_CB(self):
        if not self._sender_socket_connected:
            while True:
                try:
                    self.sender_socket.connect((self._his_host, self._his_listen_port))
                    break
                except:
                    time.sleep(0.1)
                    print("error happened while connecting to other device try again ...")
            self._sender_socket_connected = True
        while True:
            if len(self._buffer_from_dlink) > 0:
                frame = self._buffer_from_dlink.pop(0)
                print("[PhyLayer] Sending Frame", frame)
                self.sender_socket.send(frame.encode())
            time.sleep(1)

    def start(self):
        threading.Thread(target=lambda: self._send_CB(), args=()).start()
        self.listener_socket.listen()
        conn, _ = self.listener_socket.accept()
        while True:
            data = conn.recv(128).decode()
            self._buffer_to_dlink.append(PhyLayer.Frame.toFrame(data))
            print("[PhyLayer] Data read from the medium", data, "buffer size is", len(self._buffer_to_dlink))