""" extra functions and classes used by channel, receiver and sender

    Authors: Josh Bernasconi 68613585
             James Toohey    27073776
"""

from struct import *
from packet import Packet


def check_ports(*ports):
    """ Returns True if there are no duplicate ports and if all
        ports are within the acceptable range, False otherwise.
        """

    all_clear = True
    set_ports = set(ports)

    if len(ports) != len(set_ports): # Check for duplicate ports
        all_clear = False

    for port in ports: # check each port is within acceptable port range
        if port < 1024 or port > 64000 or not (isinstance(port, int)):
            all_clear = False

    return all_clear


def pack_data(packet):
    packed = pack('!2I3i' + str(packet.data_len) + 's',
                  packet.magicno, packet.checksum, packet.pac_type, packet.seqno, packet.data_len, packet.data)
    return packed


def get_header(packet):
    header = unpack('!2I3i', packet[:20])

    return header


def get_data(packet, data_len):
    data = unpack(str(data_len) + 's', packet[20:20+data_len])

    return data


def get_packets(in_data):

    packets = []

    while in_data != b'':
        header = get_header(in_data)
        # print(header)
        magic_no = header[0]
        checksum = header[1]
        pac_type = header[2]
        seq_no = header[3]
        data_len = header[4]
        data = get_data(in_data, data_len)

        # temp_packet = Packet

        if magic_no != 0x497E:
            print("MAGIC NUMBER != 0x497E, dropping packet.")
        else:
            temp_packet = Packet(pac_type, seq_no, data_len, data, checksum)
            packets.append(temp_packet)

            in_data = in_data[20+data_len:]

    return packets

def get_packet(in_data):
    """GETS A SINGLE PACKET INSTEAD OF A LIST OF PACKETS"""
    valid_packet = True

    header = get_header(in_data)
    magic_no = header[0]
    checksum = header[1]
    pac_type = header[2]
    seq_no = header[3]
    data_len = header[4]
    data = get_data(in_data, data_len)

    if magic_no != 0x497E:
        valid_packet = False
    packet = Packet(pac_type, seq_no, data_len, data, checksum)

    return packet, valid_packet, pac_type
