""" Receiver program for Cosc264 Assignment

    Does nothing yet.

    CSin_port = 7001
    CSout_port = 7002
    CRin_port = 7003
    CRout_port = 7004
    Sin_port = 7005
    Sout_port = 7006
    Rin_port = 7007
    Rout_port = 7008

    Authors: Josh Bernasconi 68613585
             James Toohey    27073776
"""

import socket
import sys
from helpers import *
from packet import Packet


def receiver(Rin_port, Rout_port, CRin_port, filename):

    ports_ok = check_ports(Rin_port, Rout_port, CRin_port)

    if ports_ok:
        print("Port numbers all valid\n")
    else:
        print("There is a problem with the supplied port numbers!\n Exiting")
        sys.exit()

    Rin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Rout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CRin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binding
    try:
        print("Binding port Rin")
        Rin.bind(('localhost', Rin_port))
        print("Rin successfully bound\n")
        print("Binding port Rout")
        Rout.bind(('localhost', Rout_port))
        print("Rout successfully bound\n")
    except socket.error as msg:
        print("Bind failed. Exiting.\n Error: " + str(msg))
        sys.exit()

    # Connecting
    try:
        print("Connecting Rout to CRin")
        Rout.connect(('localhost', CRin_port))
        print("Connection successful\n")
    except socket.error as msg:
        print("Connect failed. Exiting\n Error: " + str(msg))
        sys.exit()

    packet1 = Packet(0, 0, 27, b"Testing receiver to channel", 0)
    packed_data = pack_data(packet1)
    Rout.send(packed_data)

    Rin.close()
    Rout.close()
    CRin.close()


    return None


if __name__ == '__main__':
    print(sys.argv)
    receiver(7007, 7008, 7003, "Nothing yet")
