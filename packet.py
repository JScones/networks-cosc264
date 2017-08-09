""" A test class for packets.
    Not too sure what I'm doing
    """

class packet(object):
    def __init__(self, magicno, pacType, seqno, dataLen, data):
        self.magicno = magicno
        self.pacType = pacType
        self.seqno = seqno
        self.dataLen = dataLen
        self.data = data