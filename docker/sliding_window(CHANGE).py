import socket
import time
import struct
#^ imports for functionality

# Configuration taken from sample sender.
PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE
SWS = 100
TIMEOUT = 0.5

# data reading taken from sample sender.
def run_test():
    with open('file.mp3', 'rb') as f:
        data = f.read()

    # creates/config UDP socket taken from sender
    # IPv4, UDP, will have sliding window on top of this
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        # Binds to port 5000 for ACK's, sets timeout for ACK's to 1 second
        udp_socket.bind(("0.0.0.0", 5000))
        udp_socket.settimeout(TIMEOUT)

        # Tracking metrics
        start_time = time.time()
        packet_delays = []
        send_times = {} # Track first send time for each offset

        # Sliding Window Maintained Variables
        LAR = 0 # Last ACK Received
        LFS = 0 # Last Frame Sent
        window = {} # seq_id -> packet

        # Sending Loop
        while LAR < len(data):
            # Fills Window
            while (LFS - LAR) < SWS * MESSAGE_SIZE and LFS < len(data):
                payload = data[LFS:LFS + MESSAGE_SIZE]
                packet = struct.pack('>I', LFS) + payload

                if LFS not in send_times:
                    send_times[LFS] = time.time() #REMOVE
                
                udp_socket.sendto(packet, ('localhost', 5001))
                window[LFS] = packet
                LFS += MESSAGE_SIZE
            
            # waits for ACK's, updates ACK's received and moves window forward
            try:
                ack, _ = udp_socket.recvfrom(PACKET_SIZE)
                ack_seq = struct.unpack('>I', ack[:SEQ_ID_SIZE])[0]

                # Uses Cumulative ACK
                if ack_seq > LAR:
                    current_time = time.time() #REMOVE--
                    for offset in list(send_times.keys()):
                        if offset < ack_seq:
                            packet_delays.append(current_time - send_times[offset])
                            del send_times[offset] #REMOVE--
                    LAR = ack_seq
                    # Slide window only keeping packets that haven't been ACK'd
                    window = {seq: pkt for seq, pkt in window.items() if seq >= LAR} #REMOVE

            except socket.timeout:
                # Retransmits all packets in window on timeout
                for pkt in window.values(): 
                    udp_socket.sendto(pkt, ('localhost', 5001))

        # Sending the closing taken from sample
        total_time = time.time() - start_time
        udp_socket.sendto(struct.pack('>i', -1) + b'', ('localhost', 5001)) # Send FIN packet

        # Print metrics
        throughput = len(data) / total_time
        avg_delay = sum(packet_delays) / len(packet_delays) if packet_delays else 0
        performance = (0.3 * throughput / 1000) + (0.7 / avg_delay)
        return throughput, avg_delay, performance

if __name__ == "__main__":
    results = [run_test() for _ in range(10)]
    # Prints 3 lines, rounded to 7 decimals
    for i in range(3):
        avg = sum(r[i] for r in results) / 10
        print(f"{avg:.7f}")

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
