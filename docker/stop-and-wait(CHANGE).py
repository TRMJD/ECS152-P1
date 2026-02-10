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
server.sendto("hello client".encode('utf-8'), address) # this is a test line that must be deleted!
# start throughput timer
start_time = time.monotonic() 
# start a while loop that does not end until done sending packets
server.settimeout(TIMEOUT)
# Track per-packet delay:
# timer starts when packet is FIRST sent, ends when ACK finally received
first_send_time = {}  # seq_id(byte offset) -> time first sent
ack_time = {}         # seq_id(byte offset) -> time ack received

offset = 0 # seq id

# send file in 1020 byte chunks, stop and wait
while offset < len(raw_data): 
    payload = raw_data[offset: offset + MESSAGE_SIZE]
    packet = create_packet(offset, payload)

    if offset not in first_send_time:
        first_send_time[offset] = time.monotonic()

    try:
        # send packet
        server.sendto(packet, destination)

        # wait for ACK
        reply_packet, _client = server.recvfrom(PACKET_SIZE)
        ack_id = ack_id(reply_packet)

        # receiver ACK is cumulative "next expected byte" (byte offset)
        # this packet is considered acknowledged if ACK covers the end of this chunk
        if ack_id >= offset + len(payload):
            ack_time[offset] = time.monotonic()
            offset += len(payload)  # move forward only when this chunk is ACKed

    except socket.timeout:
        # timeout, retransmit same packet by looping again
        continue

# FIN handshake 
# send empty payload packet at final offset
eof_offset = offset
server.sendto(create_packet(eof_offset, b""), destination)

# wait for receiver's fin, send FINACK
while True:
    packet, _ = server.recvfrom(PACKET_SIZE) # _ since we do not need address of sender
    message = packet[SEQ__ID_SIZE:]
    if message == b"fin":
        server.sendto(create_packet(eof_offset, b"==FINACK=="), destination)
        break
# end timer & close socket
overall_end = time.monotonic() 
server.close()

# metrics 
total_time = overall_end - overall_start
throughput = len(raw_data) / total_time

delays = [(ack_time[s] - first_send_time[s]) for s in ack_time] # array of respective delay times
avg_delay = sum(delays) / len(delays)

metric = 0.3 * (throughput / 1000.0) + 0.7 * (1.0 / avg_delay)

# print metrics
throughput = round_up_7(throughput)
avg_delay = round_up_7(avg_delay)
metric = round_up_7(metric)

print(throughput,avg_delay,metric)


        
        
    