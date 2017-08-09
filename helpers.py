""" extra functions and classes used by channel, receiver and sender

    Authors: Josh Bernasconi 68613585
             James Toohey    27073776
"""


def check_ports(*ports):
    """ Returns True if there are no duplicate ports and if all
        ports are within the acceptable range, False otherwise.
        """

    all_clear = True
    set_ports = set(ports)

    if len(ports) != len(set_ports): #Check for duplicate ports
        all_clear = False

    for port in ports: #check each port is within acceptable port range
        if port < 1024 or port > 64000:
            all_clear = False

    return all_clear
