""" A test class for packets.
    Not too sure what I'm doing
    """

class packet(object):
    def __init__(self, magicno, pac_type, seqno, data_len, data):
        self.magicno = magicno
        self.pac_type = pac_type
        self.seqno = seqno
        self.data_len = data_len
        self.data = data
        self.checksum = self.calculate_checksum()


    def calculate_checksum(self):
        pac_type_bytes = bytearray(self.pac_type, 'utf8')
        data_bytes = bytearray(self.data, 'utf8')

        checksum = self.magicno + self.seqno + self.data_len
        for x in pac_type_bytes:
            checksum += x
        for x in data_bytes:
            checksum += x

        return checksum
