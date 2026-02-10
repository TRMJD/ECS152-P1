import socket
import time # for timing
import math # for rounding

PACKET_SIZE = 1024
# What is stop and wait over UDP?

# simple error-control for reliable data over unreliable transport layer by sending
# one packet at a time. 

# How? Sender transmits a data packet and waits for ACK before sending the next.
# Also uses timers to retransmit data if no ACK received.
SEQ__ID_SIZE = 4 # 4 bytes for seuqence ID
MESSAGE_SIZE = PACKET_SIZE - SEQ__ID_SIZE # 1020 bytes for message
TIMEOUT = 1.0 # not sure how long we must wait for timeout

# Steps
# 1. Transmit data packet
# 2. start a timer and wait
# 3. wait and receive ACK (if successful)
# 4. if receive ack stop timer and send next packet
# If timeout, retransmit packet and restart timer
# Send FIN packet when done

# convert MP3 file into data
from pydub import AudioSegment # this is a library I found https://stackoverflow.com/questions/16634128/how-to-extract-the-raw-data-from-a-mp3-file-using-python
sound = AudioSegment.from_mp3("file.mp3")
raw_data = sound._data 

# HELPER FUNCTIONS
# this is adapted from receiver.py
def create_packet(seq_id: int, payload: bytes) -> bytes:
    return int.to_bytes(seq_id, SEQ__ID_SIZE, signed=True, byteorder="big") + payload

def ack_id(ack: bytes) -> int:
    # ACK packet format: 4 byte signed seq_id + b 'ack'
    return int.from_bytes(ack_packet[:SEQ__ID_SIZE], signed=True, byteorder="big")

# create a socket 
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# destination(specified from receiver.py)
destination = ("127.0.0.1", 5001)
# send packets
server.sendto("hello client".encode('utf-8'), address) 
# start throughput timer
start_time = time.monotonic()
# start a while loop that does not end until done sending packets
server.settimeout(TIMEOUT)
while True:
    timeouts = 0
    try:
        # send packet 
        server.sendto(raw_data, destination)
        # potential ACK from client
        reply_packet, client = server.recvfrom(PACKET_SIZE) # reply packet, client because client sent it
        print("ACK Received", client)
    except socket.timeout:
        # retransmit packet


        
        
    