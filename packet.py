""" Packet Class for sender, receiver and channel.

    Authors: Josh Bernasconi 68613585
             James Toohey    27073776
    """


class Packet(object):
    def __init__(self, pac_type, seqno, data_len, data, checksum=0):
        self.magicno = 0x497E
        self.pac_type = pac_type  # integer, 0 = dataPacket, 1 = acknowledgementPacket
        self.seqno = seqno  # integer
        self.data_len = data_len  # integer
        self.checksum = checksum  # hex number
        self.data = data  # string

        if self.checksum == 0:
            self.checksum = self.calculate_checksum()

    def calculate_checksum(self):
        checksum = self.magicno + self.pac_type + self.seqno + self.data_len

        return checksum


class Header(object):
    def __init__(self, header):
        self.magicno = header[0]
        self.checksum = header[1]
        self.pac_type = header[2]
        self.seqno = header[3]
        self.datalen = header[4]
