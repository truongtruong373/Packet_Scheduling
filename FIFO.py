import random
import numpy as np

from collections import deque

N = 16
SIM_TIME = 50000
WARMUP = 5000

loads = np.arange(0.10, 0.99, 0.01)

class Packet:
    def __init__(self, arrival_time, dest):
        self.arrival_time = arrival_time
        self.dest = dest

def fifo_scheduler(input_queues):
    matched_outputs = set()
    matching = []

    for i in range(N):
        if len(input_queues[i]) == 0:
            continue

        packet = input_queues[i][0]
        if packet.dest not in matched_outputs:
            matched_outputs.add(packet.dest)
            matching.append((i, packet.dest))

    return matching

def generate_traffic(input_queues, current_time, load):
    for i in range(N):
        if random.random() < load:
            dest = random.randint(0, N - 1)
            packet = Packet(current_time, dest)
            input_queues[i].append(packet)

avg_delays = []
for load in loads:
    print(f"Running load = {load:.2f}")
    input_queues = [deque() for _ in range(N)]

    total_delay = 0
    total_departed = 0

    for t in range(SIM_TIME):
        generate_traffic(input_queues,t,load)
        matching = fifo_scheduler(input_queues)

        for i, o in matching:
            pkt = input_queues[i].popleft()
            if t > WARMUP:
                delay = t - pkt.arrival_time
                total_delay += delay
                total_departed += 1

    if total_departed > 0:
        avg_delay = total_delay / total_departed
    else:
        avg_delay = 0

    avg_delays.append(round(avg_delay, 4))

    print(f"Average Delay = {avg_delay:.3f}")

print(avg_delays)
