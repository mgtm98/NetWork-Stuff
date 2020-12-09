import threading
import time
from enum import Enum, auto
from Layer import Layer
from PhyLayer import PhyLayer

MAX_SEQ = 20


class DataLinkLayer(Layer):
    
    class _dataLinkLayerEvents(Enum):
        frame_arrival = auto()
        cksum_err = auto()
        timeout = auto()
        network_layer_ready = auto()
        no_event = auto()
    
    @staticmethod
    def _inc(i):
        if i < MAX_SEQ: i = i + 1
        else: i = 0
        return i

    @staticmethod
    def _between(a, b, c):
        if ((a <= b) and (b < c)) or ((c < a) and (a <= b)) or ((b < c) and (c < a)): return True
        else: return False

    def __init__(self, phy_layer):
        super().__init__()
        self._phy_layer:PhyLayer = phy_layer
        self._buffer_from_network_layer = self._buffer_from
        self._buffer_to_network_layer = self._buffer_to
        self._ack_expected = 0                       # next ack expected inbound 
        self._next_frame_to_send = 0                 # next frame going out 
        self._frame_expected = 0                     # number of frame expected inbound 
        self._nbuffered = 0                          # initially no packets are buffered 
        self._event:DataLinkLayer._dataLinkLayerEvents = self._dataLinkLayerEvents.no_event
        self._is_time_out = False
        self._timers = {}
    
    def add_to_buffer(self, data):
        print("[DataLink] Data added to the to buffer")
        self._buffer_from_network_layer.append(data)

    def data_available(self):
        return True if len(self._buffer_to_network_layer) > 0 else False

    def get_from_buffer(self):
        return self._buffer_to_network_layer.pop(0)

    def _wait_for_event(self):
        while True:
            time.sleep(0.25)

            if len(self._buffer_from_network_layer) > self._next_frame_to_send: self._event = self._dataLinkLayerEvents.network_layer_ready
            elif self._phy_layer.data_available(): self._event = self._dataLinkLayerEvents.frame_arrival
            elif self._is_time_out:
                self._is_time_out = False
                self._event = self._dataLinkLayerEvents.timeout
            else: pass #print("[DataLink] waiting for event ...")
            if self._event is not self._dataLinkLayerEvents.no_event: break

    def start(self):
        while True:
            self._wait_for_event()

            if self._event == self._dataLinkLayerEvents.network_layer_ready:
                self._nbuffered += 1
                frame = PhyLayer.Frame(
                    type=PhyLayer.Frame.Type.DATA,
                    info=self._buffer_from_network_layer[self._next_frame_to_send],
                    seq=self._next_frame_to_send,
                    ack=(self._frame_expected + MAX_SEQ) % (MAX_SEQ + 1)
                )
                self._start_timer(self._next_frame_to_send)
                self._phy_layer.add_to_buffer(frame)
                self._next_frame_to_send = self._inc(self._next_frame_to_send)

            elif self._event == self._dataLinkLayerEvents.frame_arrival:
                frame:PhyLayer.Frame = self._phy_layer.get_from_buffer()
                print("[DataLink] Frame Arrived", frame.toString())
                if frame.seq == self._frame_expected:
                    self._buffer_to_network_layer.append(frame.info)
                    self._frame_expected = self._inc(self._frame_expected)
                # Ack n implies n − 1, n − 2, etc. Check for this.
                while self._between(self._ack_expected, frame.ack, self._next_frame_to_send):
                    # Handle piggybacked ack.
                    self._nbuffered -= 1
                    self._stop_timer(self._ack_expected)
                    self._ack_expected = self._inc(self._ack_expected)

            elif self._event == self._dataLinkLayerEvents.cksum_err: pass

            elif self._event == self._dataLinkLayerEvents.timeout:
                self._next_frame_to_send = self._ack_expected
                for i in range(1, self._nbuffered):
                    frame = PhyLayer.Frame(
                        type=PhyLayer.Frame.Type.DATA,
                        info=self._buffer_from_network_layer[self._next_frame_to_send],
                        seq=self._frame_expected,
                        ack=(self._frame_expected + MAX_SEQ) % (MAX_SEQ + 1)
                    )
                    self._start_timer(self._next_frame_to_send, i*10)
                    self._phy_layer.add_to_buffer(frame)
                    self._next_frame_to_send = self._inc(self._next_frame_to_send)

            self._event = self._dataLinkLayerEvents.no_event

    def _start_timer(self, i, timeval=10):
        print("[DataLink] Timer({}) Started".format(i))
        def callback():
            self._is_time_out = True
            print("[DataLink] (timer{}) TimeOut".format(i))
        self._timers[i] = threading.Timer(timeval, callback)
        self._timers[i].start()

    def _stop_timer(self, i):
        print("[DataLink] Timer({}) Stoped".format(i))
        self._timers[i].cancel()
        
