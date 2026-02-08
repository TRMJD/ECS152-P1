import socket
import time
import struct
#^ imports for functionality

# Configuration taken from sample sender.
PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE
SWS = 20
TIMEOUT = 1

# data reading taken from sample sender.
with open('send.txt', 'rb') as f:
    data = f.read()

# creates/config UDP socket taken from sender
# IPv4, UDP, will have sliding window on top of this
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
    # Binds to port 5000 for ACK's, sets timeout for ACK's to 1 second
    udp_socket.bind(("0.0.0.0", 5000))
    udp_socket.settimeout(TIMEOUT)

    # Sliding Window Maintained Variables
    LAR = 0 # Last ACK Received
    LFS = 0 # Last Frame Sent
    window = {} # seq_id -> packet

    # Sending Loop
    while LAR < len(data) - 1:
        while (LFS - LAR) < SWS * MESSAGE_SIZE and LFS < len(data):
            payload = data[LFS:LFS + MESSAGE_SIZE]
            packet = struct.pack('>I', LFS) + payload
            udp_socket.sendto(packet, ('localhost', 5001))
            window[LFS] = packet
            LFS += MESSAGE_SIZE
           
        # waits for ACK's, updates ACK's received and moves window forward
        try:
            ack, _ = udp_socket.recvfrom(PACKET_SIZE)
            ack_seq = struct.unpack('>I', ack[:SEQ_ID_SIZE])[0]
            
            # Uses Cumulative ACK
            if ack_seq > LAR:
                LAR = ack_seq
                
                # Removes all ACK'd packets from window
                to_remove = [seq for seq in window if seq < LAR]
                for seq in to_remove:
                        del window[seq]

        except socket.timeout:
            # Retransmits all packets in window on timeout
            for packet in window.values(): 
                udp_socket.sendto(packet, ('localhost', 5001))

    # Sending the closing taken from sample
    fin_packet = struct.pack('>I', LFS) + b''
    udp_socket.sendto(fin_packet, ('localhost', 5001))

# Sender has up to SWS unacknowledged packets in flight

# Maintains Last ACK Received, Last Frame Sent, and LFD - LAR <= SWS

# Uses a Sender
    # Can send if window isn't full
    # Sets a timer for each packet
    # Retransmits it timer expires
    # Uses CUMULATIVE ACKS to slide window forward

# Uses a Receiver
    # Has a Receiver Window Size
    # Maintains Next Frame Expected
    # Accepts packets between NFE and NFE+RWS-1
    # Only delivers packets when all earlier ones have been received
    # Sends CUMULATIVE ACK for highest consecutive packet
