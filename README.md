# Reliable UDP File Transfer & Congestion Control

Implementation of reliable file transfer protocols over UDP using Python socket programming.

This project explores how reliable data transmission can be implemented over an unreliable transport protocol through packet sequencing, acknowledgments, retransmission logic, and performance measurement.

---

## Project Overview

The goal of this project was to implement and evaluate reliable UDP transmission under simulated network conditions using a provided Docker-based network emulation environment.

Implemented protocols include:

* Stop-and-Wait ARQ
* Fixed Sliding Window
* Additional congestion-control experiments

The sender transmits file data in fixed-size packets while tracking acknowledgments, retransmissions, throughput, and packet delay.

---

## Contributions 

Clarence D.
-----------
My primary contribution was implementing the **Stop-and-Wait reliable transfer protocol**.

This included:

* Packet construction with sequence numbering
* ACK parsing and validation
* Timeout detection
* Retransmission logic
* FIN / FINACK termination handshake
* Throughput and average packet delay measurement
* Performance metric computation

---

## Technical Concepts Demonstrated

* UDP Socket Programming
* Reliable Data Transfer
* Stop-and-Wait ARQ
* Packet Sequencing
* ACK Handling
* Timeout-Based Retransmission
* Network Performance Analysis
* Transport Layer Reliability

---

## Stop-and-Wait Protocol Workflow

1. Sender transmits a packet
2. Sender starts timeout timer
3. Receiver returns acknowledgment
4. Sender validates ACK
5. If timeout occurs, packet is retransmitted
6. Process repeats until file transfer completes
7. FIN / FINACK handshake terminates transmission

---

## Performance Metrics

The implementation measures:

### Throughput

Total bytes transmitted divided by transfer time

### Average Packet Delay

Time elapsed between first packet transmission and acknowledgment

### Performance Metric

Metric = 0.3 × (Throughput / 1000) + 0.7 × (1 / Average Delay)

---

## Environment

This project uses a Docker-based network emulation environment provided as course infrastructure for testing packet transmission behavior under simulated network conditions.

The reliable sender protocol implementation was independently developed by project contributors.

---

## Technologies Used

* Python
* UDP Sockets
* Docker
* Transport Layer Protocols
* Network Performance Measurement

---

## What I Learned

This project strengthened my understanding of:

* Reliable transport mechanisms
* How retransmission handles packet loss
* Tradeoffs between throughput and latency
* Practical implementation of transport-layer reliability over UDP

---

## Running the Project

Start the provided receiver environment:

```bash
./start-simulator.sh
```

Run sender implementation:

```bash
python sender_stop_and_wait.py
```

---

## Repository Notes

This repository contains collaborative coursework implementations.

My primary contribution focused on the Stop-and-Wait sender protocol.
