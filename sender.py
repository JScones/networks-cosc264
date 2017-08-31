""" Sender program for Cosc264 Assignment

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
import time


def sender(Sin_port, Sout_port, CSin_port, filename):
    print("SENDER\n")
    ports_ok = check_ports(Sin_port, Sout_port, CSin_port)

    if ports_ok:
        print("Port numbers all valid\n")
    else:
        print("There is a problem with the supplied port numbers!\n Exiting")
        sys.exit()

    Sin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Sout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CSin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print("Binding port Rin")
        Sin.bind(('localhost', Sin_port))
        print("Rin successfully bound\n")
        print("Binding port Rout")
        Sout.bind(('localhost', Sout_port))
        print("Rout successfully bound\n")
    except socket.error as msg:
        print("Bind failed. Exiting.\n Error: " + str(msg))
        sys.exit()

    try:
        print("Connecting Rout to CRin")
        Sout.connect(('localhost', CSin_port))
        print("Connection successful\n")
    except socket.error as msg:
        print("Connect failed. Exiting\n Error: " + str(msg))
        sys.exit()

    packet1 = Packet(0, 0, 25, b"Testing sender to channel", 0)
    packed_data = pack_data(packet1)
    Sout.send(packed_data)

    time.sleep(5)

    # packet1 = Packet(0, 0, 13, b"Second packet", 0)
    # packed_data = pack_data(packet1)
    # Sout.send(packed_data)

    Sin.close()
    Sout.close()
    CSin.close()

if __name__ == '__main__':
    sender(7005, 7006, 7001, "Filename here")
    print(sys.argv)
