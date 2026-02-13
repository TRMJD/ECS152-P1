import socket
import time
import math
# TCP Reno Algorithm described by lecture slides:
# on each new connection or after timeout, set congestion window (cwnd) to 1 MSS (message size)
# for each segment acked, increase cwnd by 1 MSS 
# if timeout then divide cwnd by 2, and set ssthresh = cwnd
# if cwnd >= ssthresh then exit slow start

# initial parameters
cwnd = 1 
ssthresh = 64
SEQ__ID_SIZE = 4 # 4 bytes for seuqence ID
MESSAGE_SIZE = PACKET_SIZE - SEQ__ID_SIZE # 1020 bytes for message
TIMEOUT = 1.0 # not sure how long we must wait for timeout

# first slow start, then AIMD, then fast retransmit, then fast recovery

# open file.mp3 and read bytes
FILE_PATH = "file.mp3"   
print("[DEBUG] Opening:", FILE_PATH)

with open("file.mp3", "rb") as f:
    raw_data = f.read()

print("[DEBUG] File loaded. Bytes:", len(raw_data))

# create a socket 
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.settimeout(TIMEOUT)
# destination(specified from receiver.py)
destination = ("127.0.0.1", 5001)
print("[DEBUG] Destination:", destination)

# metrics (copied from stop-and-wait)
overall_start = time.monotonic()
first_send_time = {}  # seq_id(byte offset) -> time first sent
ack_time = {}         # seq_id(byte offset) -> time ack received
packet_count = 0

# from sliding window.py
LAR = 0 # last ack received 
LFS = 0 # last frame sent 
window = {}

# source referenced: https://www.geeksforgeeks.org/computer-networks/tcp-reno-with-example/
# main loop: while LAR < len(raw_data), keep sending packets until all data is acked
while LAR < len(raw_data):
    # fill window with packets
    while LFS < len(raw_data) and LFS - LAR < cwnd * MESSAGE_SIZE:
        # create packet with seq_id = LFS and payload = raw_data[LFS: LFS + MESSAGE_SIZE]
        payload = raw_data[LFS: LFS + MESSAGE_SIZE] 
        packet = create_packet(LFS, payload)
        server.sendto(packet, destination) # send packet
        print(f"[DEBUG] Sent packet with seq_id {LFS}") # debug print
        if LFS not in first_send_time: # only set first send time if this is the first time sending this packet
            first_send_time[LFS] = time.monotonic()
        window[LFS] = packet # add packet to window
        LFS += len(payload) # update LFS by the size of the payload (not just 1 MSS) since we can send variable sized packets at the end
        packet_count += 1



