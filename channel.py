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

import random
import select
import socket
import sys
import time

from helpers import *


def channel(CSin_port, CSout_port, CRin_port, CRout_port, Sin_port, Rin_port, Precision):
    print("CHANNEL\n")
    random.seed(5)

    ports_ok = check_ports(CSin_port, CSout_port, CRin_port, CRout_port, Sin_port, Rin_port)

    if ports_ok:
        print("Port numbers all valid\n")
    else:
        print("There is a problem with the supplied port numbers!\n Exiting")
        sys.exit()

    # Socket init
    CSin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CSout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CRin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CRout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # TODO remove later, stops the already in use error
    CSin.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    CSout.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    CRin.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    CRout.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind
    try:  # Catching errors binding the ports
        print("Binding port CSin")
        CSin.bind(('localhost', CSin_port))
        print("CSin successfully bound\n")
        print("Binding port CSout")
        CSout.bind(('localhost', CSout_port))
        print("CSout successfully bound\n")
        CRin.bind(('localhost', CRin_port))
        print("CRin successfully bound\n")
        CRout.bind(('localhost', CRout_port))
        print("CRout successfully bound\n")
    except socket.error as msg:
        print("Bind failed. Exiting.\n Error: " + str(msg))
        sys.exit()

    # Listen and accept CSin
    CSin.listen(50)
    CSin, _ = CSin.accept()

    print("CSin accepted")

    # Connect CRout to Rin
    connected = False
    connect_attempts = 0
    while not connected:
        try:
            print("Connecting CRout to Rin")
            CRout.connect(('localhost', Rin_port))
            print("Connection successful\n")
            connected = True
        except socket.error as msg:
            connect_attempts += 1
            if msg.errno == 111 and connect_attempts < 6:
                print("Connection refused {} time(s), sleeping and retrying".format(connect_attempts))
                time.sleep(5)
                pass
            else:
                print("Connect failed. Exiting\n Error: " + str(msg))
                sys.exit()

    # Listen and accept CRin
    CRin.listen(50)
    CRin, _ = CRin.accept()

    # Connect CSout to Sin
    try:
        print("Connecting CSout to Sin")
        CSout.connect(('localhost', Sin_port))
        print("Connection successful\n")
    except socket.error as msg:
        print("Connect failed. Exiting\n Error: " + str(msg))
        sys.exit()

    # Receive, select and send
    receive(CSin, CSout, CRin, CRout, CSin_port, CRin_port, Precision)

    CSin.close()
    CSout.close()
    CRin.close()
    CRout.close()
    return None

def receive(CSin, CSout, CRin, CRout, CSin_port, CRin_port, Precision):
    """Big fuckoff function, will be refactored"""
    finished = False
    while not finished:  # while CRin doesnt receive terminating packet
        readable, _, _ = select.select([CSin, CRin], [], [])
        for sock in readable:
            host, port = sock.getsockname()
            if port == CSin_port:
                data_in, address = sock.recvfrom(1024)

                if len(data_in) != 0:
                    header = get_header_object(data_in)

                    if header.magicno != 0x497E:
                        print("Sender Packet magic number != 0x497E, dropping packet.\n")
                        continue
                    else:
                        u = random.uniform(0, 1)
                        if u < Precision:  # bit errors
                            print("bit error")
                            packet, valid = get_packet(data_in)
                            if valid:
                                new_packet = Packet(packet.pac_type,
                                                    packet.seqno,
                                                    packet.data_len + random.randrange(0, 11),
                                                    packet.data,
                                                    packet.checksum)
                                data_in = pack_data(new_packet)
                        else:
                            v = random.uniform(0, 1)
                            if v < 0.1:
                                print("drop packet")
                                continue
                        CRout.send(data_in)
                else:
                    print("empty data packet received, finished")
                    finished = True
                    break

            elif port == CRin_port:
                data_in, address = sock.recvfrom(1024)

                if len(data_in) != 0:
                    header = get_header_object(data_in)
                    if header.magicno != 0x497E:
                        print("Receiver Packet magic number != 0x497E, dropping packet.\n")
                    else:
                        # Random variant for packet loss and bit errors to be implemented
                        CSout.send(data_in)
                else:
                    # TODO does this ever get called?
                    print("nothing received from receiver, done")
                    finished = True
                    break


if __name__ == '__main__':
    channel(7001, 7002, 7003, 7004, 7005, 7007, 0.1)
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
