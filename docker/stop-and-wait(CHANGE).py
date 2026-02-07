# What is stop and wait over UDP?

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


# start a while loop that does not end until done sending packets
while true:
    # send packets
    socket.sendto() 