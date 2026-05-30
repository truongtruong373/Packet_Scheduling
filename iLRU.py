import random
import numpy as np

from collections import deque

N = 16
SIM_TIME = 50000
WARMUP = 5000
ITERATIONS = 1

loads = np.arange(0.10, 0.99, 0.10)

class Packet:
    def __init__(self, arrival_time, dest):
        self.arrival_time = arrival_time
        self.dest = dest

def ilru_scheduler(voq, last_input_served, last_output_served, current_time, iterations=1):
    matching = []
    matched_inputs = set()
    matched_outputs = set()

    for _ in range(iterations):

        # REQUEST
        requests = [[] for _ in range(N)]
        for i in range(N):
            if i in matched_inputs:
                continue
            for o in range(N):
                if o in matched_outputs:
                    continue
                if len(voq[i][o]) > 0:
                    requests[o].append(i)

        # GRANT
        grants = {}
        for o in range(N):
            for o in matched_outputs:
                continue
            if len(requests[o]) == 0:
                continue

            select_input = requests[o][0]
            oldest_time = last_input_served[select_input]
            for candidate in requests[o]:
                if last_input_served[candidate] < oldest_time:
                    oldest_time = last_input_served[candidate]
                    select_input = candidate

            grants[o] = select_input

        # ACCEPT
        for i in range(N):
            if i in matched_inputs:
                continue
            granted_outputs = []

            for o, granted_input in grants.items():
                if granted_input == i:
                    granted_outputs.append(o)

            if len(granted_outputs) == 0:
                continue

            selected_output = granted_outputs[0]
            oldest_time = last_output_served[selected_output]

            for candidate in granted_outputs:

                if last_output_served[candidate] < oldest_time:
                    oldest_time = last_output_served[candidate]
                    selected_output = candidate

            matching.append((i, selected_output))
            matched_inputs.add(i)
            matched_outputs.add(selected_output)

            last_input_served[i] = current_time
            last_output_served[i] = current_time

    return matching

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
    last_input_served = [0] * N
    last_output_served = [0] * N
    total_delay = 0
    total_departed = 0

    for t in range(SIM_TIME):
        generate_traffic(voq,t,load)

        matching = ilru_scheduler(voq, last_input_served, last_output_served, t, iterations=ITERATIONS)

        for i, o in matching:
            if len(voq[i][o]) == 0:
                continue

            packet = voq[i][o].popleft()
            if t > WARMUP:
                delay = (t - packet.arrival_time)
                total_delay += delay
                total_departed += 1

    if total_departed > 0:
        avg_delay = (total_delay / total_departed)
    else:
        avg_delay = 0

    avg_delays.append(avg_delay)

    print(f"Average Delay = {avg_delay:.3f}")

print(avg_delays)
