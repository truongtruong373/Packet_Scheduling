import random
import numpy as np

from collections import deque

N = 16
SIM_TIME = 50000
WARMUP = 5000

loads = np.arange(0.5, 0.99, 0.02)

class Packet:
    def __init__(self, arrival_time, dest):
        self.arrival_time = arrival_time
        self.dest = dest

def msm_scheduler(voq):
    graph = [[] for _ in range(N)]
    for i in range(N):
        for o in range(N):
            if len(voq[i][o]) > 0:
                graph[i].append(o)

    match_output = [-1] * N

    def dfs(input_port, visited):
        for output_port in graph[input_port]:
            if visited[output_port]:
                continue

            visited[output_port] = True

            if match_output[output_port] == -1:
                match_output[output_port] = input_port
                return True

            previous_input = match_output[output_port]

            if dfs(previous_input, visited):
                match_output[output_port] = input_port
                return True

        return False

    for input_port in range(N):
        visited = [False] * N
        dfs(input_port,visited)

    matching = []
    for output_port in range(N):
        if match_output[output_port] != -1:
            matching.append((match_output[output_port],output_port))

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

    total_delay = 0
    total_departed = 0

    for t in range(SIM_TIME):

        generate_traffic(voq, t, load)

        matching = msm_scheduler(voq)

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