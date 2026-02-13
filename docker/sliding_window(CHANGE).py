import socket
import time
import struct
#^ imports for functionality

# Configuration taken from sample sender.
PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE
SWS = 100
TIMEOUT = 2.0

# data reading taken from sample sender.
def run_test():
    with open('file.mp3', 'rb') as f:
        data = f.read()

    # Start timer when socket is created
    start_time = time.time()

    # creates/config UDP socket taken from sender
    # IPv4, UDP, will have sliding window on top of this
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        # Binds to port 5000 for ACK's, sets timeout for ACK's to 1 second
        udp_socket.bind(("0.0.0.0", 5000))
        udp_socket.settimeout(TIMEOUT)

        # Tracking metrics
        packet_delays = []
        send_times = {} # Track first send time for each offset

        # Sliding Window Maintained Variables
        LAR = 0 # Last ACK Received
        LFS = 0 # Last Frame Sent
        window = {} # seq_id -> packet
        timeouts = 0

        # Sending Loop
        while LAR < len(data):
            # Fills Window
            while (LFS - LAR) < SWS * MESSAGE_SIZE and LFS < len(data):
                payload = data[LFS:LFS + MESSAGE_SIZE]
                packet = struct.pack('>I', LFS) + payload
                if LFS not in send_times:
                    send_times[LFS] = time.time()

                udp_socket.sendto(packet, ('localhost', 5001))
                window[LFS] = packet
                LFS += MESSAGE_SIZE

            # waits for ACK's, updates ACK's received and moves window forward
            try:
                ack, _ = udp_socket.recvfrom(PACKET_SIZE)
                ack_seq = struct.unpack('>I', ack[:SEQ_ID_SIZE])[0]

                # Uses Cumulative ACK
                if ack_seq > LAR:
                    current_time = time.time()
                    ackd_offsets = [off for off in list(send_times.keys()) if off < ack_seq]
                    for offset in ackd_offsets:
                        packet_delays.append(current_time - send_times[offset])
                        del send_times[offset]
                        if offset in window:
                            del window[offset]
                    LAR = ack_seq
                    # Resets timeouts on success
                    timeouts = 0 

            except socket.timeout:
                timeouts += 1
                # Retransmits all packets in window on timeout
                if timeouts > 100: 
                        return 0, 0, 0 
                current_window_seqs = sorted(window.keys())
                for seq_key in current_window_seqs:
                        if seq_key in window: 
                                        udp_socket.sendto(window[seq_key], ('localhost', 5001))


        # Sending the closing taken from sample
        total_time = time.time() - start_time
        for _ in range(5):
                # Send FIN Packet
                udp_socket.sendto(struct.pack('>i', -1) + b'==FINACK==', ('localhost', 5001))

        # Print metrics
        throughput = len(data) / total_time
        avg_delay = sum(packet_delays) / len(packet_delays) if packet_delays else 0
        performance = (0.3 * throughput / 1000) + (0.7 / avg_delay)
        return throughput, avg_delay, performance

if __name__ == "__main__":
    t, d, m = run_test()
    # Prints 3 lines, rounded to 7 decimals
    print(f"{t:.7f}")
    print(f"{d:.7f}")
    print(f"{m:.7f}")

# Performance Metrics       (Throughput, Average Delay, Performance)
    # Averages:             92989.58989584, 1.08521647, 28.54343032
    # Standard Deviations:  4917.5367449, 0.0569122, 1.5069661

