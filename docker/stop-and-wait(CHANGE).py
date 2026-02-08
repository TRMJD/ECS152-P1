import socket
PACKET_SIZE = 1024
# What is stop and wait over UDP?
SEQ__ID_SIZE = 4 # 4 bytes for seuqence ID
MESSAGE_SIZE = PACKET_SIZE - SEQ__ID_SIZE # 1020 bytes for message


# simple error-control for reliable data over unreliable transport layer by sending
# one packet at a time. 

# How? Sender transmits a data packet and waits for ACK before sending the next.
# Also uses timers to retransmit data if no ACK received.

# Steps
# 1. Transmit data packet
# 2. start a timer and wait
# 3. receive ACK (if successful)
# 4. if receive ack stop timer and send next packet

# convert MP3 file into data
from pydub import AudioSegment # this is a library I found https://stackoverflow.com/questions/16634128/how-to-extract-the-raw-data-from-a-mp3-file-using-python
sound = AudioSegment.from_mp3("file.mp3")
raw_data = sound._data

# create a socket 
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind to IPv4 Address and port (specified from receiver.py)
server.bind(("0.0.0.0", 5001))
# send packets
server.sendto("hello client".encode('utf-8'), address) 

# start a while loop that does not end until done sending packets
while true:
    timeouts = 0
    try:
        message, address = server.recvfrom(PACKET_SIZE)
        
# Noah's Contributions using DISC reference [<- Remember to DELETE THIS!!!]
# Send one packet
# Start timer
# Wait for ACK
# If ACK received, stop timer and send next packet
# If timeout, retransmit packet and restart timer
# Send FIN packet when done

    