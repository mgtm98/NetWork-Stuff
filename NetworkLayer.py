from Layer import Layer
from DataLink import DataLinkLayer
import time

class NetworkLayer(Layer):
    def __init__(self, dlink_layer):
        super().__init__()
        self._dlink_layer:DataLinkLayer = dlink_layer
    
    def start(self):
        while True:
            self._dlink_layer.add_to_buffer("Frame0")
            time.sleep(5)
            self._dlink_layer.add_to_buffer("Frame1")
            time.sleep(5)
            self._dlink_layer.add_to_buffer("Frame2")
            time.sleep(5)
            self._dlink_layer.add_to_buffer("Frame3")
            time.sleep(5)