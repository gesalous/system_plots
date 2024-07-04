import matplotlib.pyplot as plt
import sys

def parse_mpstat(file, cpu_id):
    data = {
        'time': [],
        'usr': [],
        'sys': [],
        'iowait': [],
        'irq': [],
        'soft': [],
        'idle': []
    }

    with open(file, 'r') as f:
        lines = f.readlines()

    # Find the header line and get indices for the required columns
    header = None
    for line in lines:
        if '%usr' in line:
            header = line.split()
            break

    if not header:
        print('Error: Could not find header line containing "CPU"')
        sys.exit(1)

    # Get indices of the required fields
    time_idx = header.index('CPU') - 1
    usr_idx = header.index('%usr')
    sys_idx = header.index('%sys')
    iowait_idx = header.index('%iowait')
    irq_idx = header.index('%irq')
    soft_idx = header.index('%soft')
    idle_idx = header.index('%idle')

    # Parse the lines to find the required CPU data
    for line in lines:
        if line.strip().startswith('Linux') or line.strip() == '':
            continue
        parts = line.split()
        if parts[1] == cpu_id or (cpu_id == 'all' and parts[1] == 'all'):
            data['time'].append(parts[time_idx])
            data['usr'].append(float(parts[usr_idx].replace(',', '.')))
            data['sys'].append(float(parts[sys_idx].replace(',', '.')))
            data['iowait'].append(float(parts[iowait_idx].replace(',', '.')))
            data['irq'].append(float(parts[irq_idx].replace(',', '.')))
            data['soft'].append(float(parts[soft_idx].replace(',', '.')))
            data['idle'].append(float(parts[idle_idx].replace(',', '.')))

    return data

def plot_cpu_stats(data, cpu_id, output_file):
    time = range(len(data['time']))

    plt.figure(figsize=(10, 6))
    plt.plot(time, data['usr'], label='%usr')
    plt.plot(time, data['sys'], label='%sys')
    plt.plot(time, data['iowait'], label='%iowait')
    plt.plot(time, data['irq'], label='%irq')
    plt.plot(time, data['soft'], label='%soft')
    plt.plot(time, data['idle'], label='%idle')

    plt.xlabel('Relative Time (s)')
    plt.ylabel('Percentage')
    plt.title(f'CPU {cpu_id} Usage Over Time')
    plt.yticks(range(0, 101, 10))  # Setting y-axis ticks from 0 to 100
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)  # Save plot to PDF file
    plt.close()  # Close the plot to free up memory

def main():
    if len(sys.argv) != 4:
        print('Usage: python script.py <filename> <cpu_id> <output_file.pdf>')
        sys.exit(1)

    filename = sys.argv[1]
    cpu_id = sys.argv[2]
    output_file = sys.argv[3]

    data = parse_mpstat(filename, cpu_id)
    plot_cpu_stats(data, cpu_id, output_file)

if __name__ == '__main__':
    main()

