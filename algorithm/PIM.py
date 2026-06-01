import random
import numpy as np

from collections import deque

N = 16
SIM_TIME = 50000
WARMUP = 5000
ITERATIONS = 1

loads = np.arange(0.10, 0.99, 0.01)

class Packet:
    def __init__(self, arrival_time, dest):
        self.arrival_time = arrival_time
        self.dest = dest

def pim_scheduler(voq, iterations=1):

    matched_inputs = set()
    matched_outputs = set()
    matching = []

    for _ in range(iterations):

        # REQUEST
        requests = {j: [] for j in range(N)}
        for i in range(N):
            if i in matched_inputs:
                continue
            for o in range(N):
                if o in matched_outputs:
                    continue
                if len(voq[i][o]) > 0:
                    requests[o].append(i)

        # GRANT
        grants = {j: [] for j in range(N)}
        for o in range(N):
            if o in matched_outputs:
                continue
            if len(requests[o]) > 0:
                granted_input = random.choice(requests[o])
                grants[granted_input].append(o)

        # ACCEPT
        for i in range(N):
            if i in matched_inputs:
                continue
            if len(grants[i]) > 0:
                accept_output = random.choice(grants[i])
                matched_inputs.add(i)
                matched_outputs.add(accept_output)
                matching.append((i, accept_output))

    return matching

# BERNOULLI

def generate_traffic(voq, current_time, load):
    for input_port in range(N):
        if random.random() < load:
            output_port = random.randint(0, N-1)
            packet = Packet(current_time, output_port)
            voq[input_port][output_port].append(packet)

avg_delays = []
for load in loads:
    print(f"Running load = {load:.2f}")

    voq = [[deque() for _ in range(N)] for _ in range(N)]

    total_delay = 0
    total_departed = 0

    for t in range(SIM_TIME):
        generate_traffic(voq, t, load)
        matching = pim_scheduler(voq,iterations=ITERATIONS)

        for i, o in matching:
            if len(voq[i][o]) > 0:
                packet = voq[i][o].popleft()
                if t > WARMUP:
                    delay = t - packet.arrival_time
                    total_delay += delay
                    total_departed += 1

    if total_departed > 0:
        avg_delay = total_delay / total_departed
    else:
        avg_delay = 0

    avg_delays.append(round(avg_delay, 4))
    print(f"Average Delay = {avg_delay:.3f}")

print(avg_delays)
