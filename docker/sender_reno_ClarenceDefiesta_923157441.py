import socket
import time
# TCP Reno Algorithm described by lecture slides:
# on each new connection or after timeout, set congestion window (cwnd) to 1 MSS (message size)
# for each segment acked, increase cwnd by 1 MSS 
# if timeout then divide cwnd by 2, and set ssthresh = cwnd
# if cwnd >= ssthresh then exit slow start

# initial parameters
cwnd = 1 
ssthresh = 64

# first slow start, then AIMD, then fast retransmit, then fast recovery

# open file.mp3 and read bytes
FILE_PATH = "file.mp3"   
print("[DEBUG] Opening:", FILE_PATH)

with open("file.mp3", "rb") as f:
    raw_data = f.read()

print("[DEBUG] File loaded. Bytes:", len(raw_data))

# create a socket 
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# destination(specified from receiver.py)
destination = ("127.0.0.1", 5001)
print("[DEBUG] Destination:", destination)

# influence from sliding window.py
LAR = 0 # last ack received 
LFS = 0 # last frame sent 

while LAR < len(raw_data):
    # fill window with packets



