""" Channel program for Cosc264 Assignment

    Does nothing yet.

    Authors: Josh Bernasconi 68613585
             James Toohey    27073776
"""

import socket
import sys

def channel(CSin, CSout, CRin, CRout, Sin, Rin, Precision):

    return None


if __name__ == '__main__':
    print(sys.argv)
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

        channel(CSin, CSout, CRint, CRout, Sin, Rin, Precision)
