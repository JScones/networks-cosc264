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
import select
from helpers import *
from packet import Packet


def receiver(Rin_port, Rout_port, CRin_port, filename):
    print("RECEIVER\n")
    ports_ok = check_ports(Rin_port, Rout_port, CRin_port)

    if ports_ok:
        print("Port numbers all valid\n")
    else:
        print("There is a problem with the supplied port numbers!\n Exiting")
        sys.exit()

    file = open(filename, "w")  # Should this be a or w?
    expected = 0

    # Socket init
    Rin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Rout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CRin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # Bind
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

    # Listen and accept Rin
    Rin.listen(50)
    Rin, _ = Rin.accept()

    # Connect Rout to CRin
    try:
        print("Connecting Rout to CRin")
        Rout.connect(('localhost', CRin_port))
        print("Connection successful\n")
    except socket.error as msg:
        print("Connect failed. Exiting\n Error: " + str(msg))
        sys.exit()

    # Read/Write
    while True: # while the empty packet has not been found
        readable, _, _ = select.select([Rin], [], [])
        if len(readable) == 1:
            data_in, address = readable[0].recvfrom(1024)
            rcvd, valid_packet, pac_type = get_packet(data_in)
            if not valid_packet:
                print("Different magic number stop processing\n")
            elif pac_type == 1:
                print("Packet type not dataPacket, stop processing\n")

            # Preparing acknowledgement packets.
            elif rcvd.seqno != expected:
                packet = Packet(1, rcvd.seqno, 0, "idk") # Still needs a data parameter. Page 6
                acknowledgement_packet = pack_data(packet)
                Rout.send(acknowledgement_packet)
            elif rcvd.seqno == expected:
                packet = Packet(1, rcvd.seqno, 0, "")
                acknowledgement_packet = pack_data(packet)
                Rout.send(acknowledgement_packet)
            if rcvd.data_len > 0:
                print(rcvd.data)
                file.write(rcvd.data)
            else:
                Rin.close()
                Rout.close()
                CRin.close()
                break




    """
    packet1 = Packet(0, 0, 27, b"Testing receiver to channel", 0)
    packed_data = pack_data(packet1)
    Rout.send(packed_data)"""

    return None


if __name__ == '__main__':
    print(sys.argv)
    receiver(7007, 7008, 7003, "out.txt")
