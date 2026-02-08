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
