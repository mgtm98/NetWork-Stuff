import threading
import time
from PhyLayer import PhyLayer
from DataLink import DataLinkLayer
from NetworkLayer import NetworkLayer

if __name__ == "__main__":
    print("wait for device 2 to start")
    time.sleep(3)
    print("------------- Init Device 1 ----------------------")
    phy = PhyLayer("127.0.0.1", 7000, "127.0.0.1", 7001)
    dlink = DataLinkLayer(phy)
    network = NetworkLayer(dlink)

    phy_thread = threading.Thread(target=lambda: phy.start(), args=())
    dlink_thread = threading.Thread(target=lambda: dlink.start(), args=())
    network_thread = threading.Thread(target=lambda: network.start(), args=())

    phy_thread.start()
    dlink_thread.start()
    network_thread.start()