# Data Link Layer - Protocol 5 
###### Inspired by ***Computer Networks - A Tanenbaum - 5th edition***  by ANDREW S. TANENBAUM & DAVID J. WETHERALL
## Code Design 
The code is divided to several Classes each represents a layer in the OSI model layers

 1. Physical Layer
 2. Data Link Layer
 3. Network Layer

Every Layer is represented as a class and each class inherits from Abstract Layer class which abstracts the communication between the different layers

## Communication between Layers

Layers classes inherit from Layer class which defines buffers & communication methods between the layers

![Alt text](https://github.com/mgtm98/NetWork-Stuff/blob/main/Untitled%20Diagram.png)

#### Layer Abstract Class
```python
self._buffer_from = [] # represents the data sent from the higher layer  
self._buffer_to   = [] # represents the data that can fetched by the higher layer
# Methods ...
def add_to_buffer(self, data) # used by the higher layer to send data to the lower layer   
def data_available(self)      # used by the higher layer to fetch data from the lower layer
def get_from_buffer(self)     # used to check if there is available data to be fetched by the higher layer  
def start(self)               # the main method in the layer 
```
#### Physical Layer
Phy layer implementation depends on 
- socket programming techniques to represent the actual physical layer and simulate propagation & processing delays
- Multithreading to simulate the concurrency between the different layers 
#### Devices scripts
- Represents a full device with it's 3 layers (PhyLayer - DataLink Layer - Network Layer) 
- every device is given a port to communicate with the other device
