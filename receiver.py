""" Receiver program for Cosc264 Assignment

    Does nothing yet.

    Authors: Josh Bernasconi 68613585
             James Toohey    27073776
"""

import socket
import sys
from helpers import check_ports


def receiver(Rin_port, Rout_port, CRin_port, filename):

    ports_ok = check_ports(Rin_port, Rout_port, CRin_port)

    if ports_ok:
        print("Port numbers all valid\n")
    else:
        print("There is a problem with the supplied port numbers!\n Exiting")
        sys.exit()

    Rin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Rout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

    try:
        print("Connecting Rout to CRin")
        Rout.connect(('localhost', CRin_port))
        print("Connection successful\n")
    except socket.error as msg:
        print("Connect failed. Exiting\n Error: " + str(msg))
        sys.exit()



    return None


if __name__ == '__main__':
    print(sys.argv)
    receiver(5555, 5556, 7777, "Nothing yet")
