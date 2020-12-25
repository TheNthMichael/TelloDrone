#   Michael Nickerson 12/25/2020
#   Description:
#       Class for handling Tello
#       Drone connections and 
#       controls

import threading
import socket
import sys
import time

"""
Tello Drone Class
    Handles setting up the connection
    to the drone and sending commands.

    Class is handled as a singleton
    so that only one connection can
    be made at a time.

    Tello drone address and port are
    supposed to be fixed at
    address = '192.168.10.1'
    port = 8889

    We can should be able to receive
    drone data through
    (data, server) = sock.recvfrom(1518)
"""
class TelloDrone:
    _TelloDrone = None
    def __init__(self, localaddr_tuple, droneaddr_tuple):
        if TelloDrone._TelloDrone == None:
            # (addr, port)
            self.localaddr = localaddr_tuple
            # (addr, port)
            self.droneaddr = droneaddr_tuple
            self.local_socket = socket.socket(socket.AF_INET,\
                socket.SOCK_DGRAM)
            self.local_socket.bind(self.localaddr)
            try:
                TelloDrone._TelloDrone = self

            except Exception as e:
                print("Exception in TelloDrone.__init__\
                (self, host, port), " + e)
                raise e
        else:
            raise Exception("Exception in TelloDrone.__init__\
                (self, host, port), An instance of the TelloDrone\
                singleton class already exists.")