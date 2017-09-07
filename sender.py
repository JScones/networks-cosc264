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
import select
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

    file = open(filename, "r")  # Check it exists. If not, exit.
    next = 0
    exit_flag = False

    # Socket init
    Sin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Sout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CSin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind
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

    # Connect Sout
    try:
        print("Connecting Sout to CSin")
        Sout.connect(('localhost', CSin_port))
        print("Connection successful\n")
    except socket.error as msg:
        print("Connect failed. Exiting\n Error: " + str(msg))
        sys.exit()

    # Listen and Accept Sin
    Sin.listen(50)
    Sin, _ = Sin.accept()

    # Test write...
    #packet1 = Packet(1, 0, 25, "Testing sender to reciever", 0)
    #packed_data = pack_data(packet1)
    #Sout.send(packed_data)
    #print("Packet sent")


    # Read/Write
    bytes = file.read(512)
    n = len(bytes)
    while True:
        if n == 0:
            packet = Packet(0, next, 0, '')
            data_packet = pack_data(packet)
        else:
            packet = Packet(0, next, n, bytes)
            data_packet = pack_data(packet)

        # To be start of inner loop
        Sout.send(data_packet)
        readable, _, _ = select.select([Sin], [], [])  # Timeout after 1 second. If timeout, retransmit.

        if len(readable) == 1:
            data_in, address = readable[0].recvfrom(1024)
            rcvd, valid_packet, pac_type = get_packet(data_in)
            if valid_packet and rcvd.type == 1 and rcvd.data_len == 0 and rcvd.seqno == next:
                next = 1 - next
                print("Recieved acknowledgement packet.")
                if exit_flag == True:  # Go to beginning of outer loop
                    file.close()
                    break
                # else: back to beginning of loop without closing.
                # A counter for how many packets are sent is also to be added.

    # time.sleep(5)


    Sin.close()
    Sout.close()
    CSin.close()

if __name__ == '__main__':
    sender(7005, 7006, 7001, "in.txt")
    print(sys.argv)
