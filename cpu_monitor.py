#!/usr/bin/env python3

import os
import sys
import subprocess
from typing import List, Dict
import matplotlib.pyplot as plt

def generate_mpstat(filename: str) -> None:
    try:
        with open(filename, 'w') as file:
            subprocess.run(['mpstat', '-P', 'ALL', '1', '5'], stdout=file, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error generating mpstat output: {e}')
        sys.exit(1)

def parse_mpstat(file: str, cpu_id: str) -> Dict[str, List[float]]:
    data = {key: [] for key in ['time', 'usr', 'sys', 'iowait', 'irq', 'soft', 'idle']}

    try:
        with open(file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f'Error: File {file} not found')
        sys.exit(1)

    header = next((line.split() for line in lines if '%usr' in line), None)
    if not header:
        print('Error: Could not find header line containing "CPU"')
        sys.exit(1)

    indices = {key: header.index(f'%{key}') for key in data if key != 'time'}
    time_idx = header.index('CPU') - 1

    for line in lines:
        parts = line.split()
        if len(parts) > 1 and (parts[1] == cpu_id or (cpu_id == 'all' and parts[1] == 'all')):
            data['time'].append(parts[time_idx])
            for key, idx in indices.items():
                data[key].append(float(parts[idx].replace(',', '.')))

    return data

def plot_cpu_stats(data: Dict[str, List[float]], cpu_id: str, output_file: str) -> None:
    time = range(len(data['time']))

    plt.figure(figsize=(10, 6))
    for key in data:
        if key != 'time':
            plt.plot(time, data[key], label=f'%{key}')

    plt.xlabel('Relative Time (s)')
    plt.ylabel('Percentage')
    plt.title(f'CPU {cpu_id} Usage Over Time')
    plt.yticks(range(0, 101, 10))
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    plt.close()

def main() -> None:
    filename = 'mpstat_output.txt'
    cpu_id = sys.argv[1] if len(sys.argv) > 1 else 'all'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'output.pdf'

    generate_mpstat(filename)
    data = parse_mpstat(filename, cpu_id)
    plot_cpu_stats(data, cpu_id, output_file)

    os.remove(filename)

if __name__ == '__main__':
    main()
