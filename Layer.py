class Layer:
    def __init__(self):
        self._buffer_from = []
        self._buffer_to = []
    
    def add_to_buffer(self, data):
        self._buffer_from.append(data)

    def data_available(self):
        return True if len(self._buffer_to) > 0 else False

    def get_from_buffer(self):
        return self._buffer_to.pop(0)

    def start(self):
        pass