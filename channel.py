""" Channel program for Cosc264 Assignment

    Does nothing yet.

    CSin_port = 7001
    CSout_port = 7002
    CRin_port = 7003
    CRout_port = 7004
    Sin_port = 7005
    Rin_port = 7006

    Authors: Josh Bernasconi 68613585
             James Toohey    27073776
"""

import socket
import sys
import select
from packet import Packet
from helpers import *


def channel(CSin_port, CSout_port, CRin_port, CRout_port, Sin_port, Rin_port, Precision):
    print("CHANNEL\n")

    ports_ok = check_ports(CSin_port, CSout_port, CRin_port, CRout_port, Sin_port, Rin_port)

    if ports_ok:
        print("Port numbers all valid\n")
    else:
        print("There is a problem with the supplied port numbers!\n Exiting")
        sys.exit()

    CSin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CSout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CRin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CRout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try: # Catching errors binding the ports
        print("Binding port CSin")
        CSin.bind(('localhost', CSin_port))
        print("CSin successfully bound\n")
        print("Binding port CSout")
        CSout.bind(('localhost', CSout_port))
        print("CSout successfully bound\n")
        CRin.bind(('localhost', CRin_port))
        print("CRin successfully bound\n")
        CRout.bind(('localhost', CRout_port))
        print("CRout successfully bound")
    except socket.error as msg:
        print("Bind failed. Exiting.\n Error: " + str(msg))
        sys.exit()

    CRin.listen(50)
    CSin.listen(50)

    CRin, _ = CRin.accept()
    CSin, _ = CSin.accept()

    while True:
        readable, _, _ = select.select([CSin], [], [])
        for sock in readable:
            data_in, address = sock.recvfrom(1024)
            rcvd, valid_packet, _ = get_packet(data_in)
            if not valid_packet:
                 print("Packet magic number != 0x497E, dropping packet.\n")
            else:
                # Random variant for packet loss and bit errors to be implemented
                CRout.send(pack_data(rcvd))
        exit = input("Type EC to exit channel")
        if exit == "EC":
            break
        temp = input("Press enter to exit")

    """ SCONZ CODE FROM LAST USE
    while True:

        readable, _, _ = select.select([CRin, CSin],[],[])

        if len(readable) != 0:
            for sock in readable:
                #print(sock)
                in_packet, address = sock.recvfrom(1024)
                if len(in_packet) != 0:
                    header, data = unpack_data(in_packet)
                    print("header = "+ str(header))
                    #print(data.decode())
        readable = []

        temp = input("Pausing loop, press enter to step")
        if temp == "b":
            break;
    temp = input("Press enter to exit")
    """
    CSin.close()
    CSout.close()
    CRin.close()
    CRout.close()
    return None


if __name__ == '__main__':
    channel(7001,7002,7003,7004,7005,7007,1)
    # uncomment below to get command line args working again
    """
    if len(sys.argv) != 8:
        print("Invalid command.")
        print("Usage: channel.py [CSin port] [CSout port] [CRin port] [CRout port] {Sin port] [Rin port] [Precision]")
    else:
        CSin = sys.argv[1]
        CSout = sys.argv[2]
        CRin = sys.argv[3]
        CRout = sys.argv[4]
        Sin = sys.argv[5]
        Rin = sys.argv[6]
        Precision = sys.argv[7]

        channel(CSin, CSout, CRin, CRout, Sin, Rin, Precision)
    """