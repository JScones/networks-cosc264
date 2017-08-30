""" A test class for packets.
    Not too sure what I'm doing

    Example usage:
    packet1 = packet(0, 0, 512, "Testing some stuff")
    print(hex(packet1.checksum))
    """

from helpers import *


class Packet(object):

    def __init__(self, pac_type, seqno, data_len, data):
        self.magicno = 0x497E
        self.pac_type = pac_type  # integer, 0 = dataPacket, 1 = acknowledgementPacket
        self.seqno = seqno  # integer
        self.data_len = data_len  # integer
        self.checksum = self.calculate_checksum() # hex number
        self.data = data  # string

    def calculate_checksum(self):

        checksum = self.magicno + self.pac_type + self.seqno + self.data_len

        return checksum

"""
if __name__ == "__main__":

    packet1 = Packet(0, 0, 4, 'test'.encode('utf-8'))
    print(packet1.checksum)
    print(hex(packet1.checksum))
    packed_data = pack_data(packet1)
    print(packed_data)
    header, data = unpack_data(packed_data)
    print(header)
    print(data.decode())
"""